package service

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"time"

	"github.com/AkariGroup/akari_software/internal/akira/system"
)

type containerConfigFactory interface {
	createContainerConfig() (system.CreateContainerOption, interface{}, error)
}

type ServiceContainer struct {
	fa     containerConfigFactory
	d      *system.DockerSystem
	status ServiceStatus

	containerId     *system.ContainerId
	containerConfig system.CreateContainerOption
	containerMeta   interface{}

	mu sync.Mutex
}

func NewServiceContainer(fa containerConfigFactory, d *system.DockerSystem) *ServiceContainer {
	return &ServiceContainer{
		fa:     fa,
		d:      d,
		status: Terminated,
	}
}

func goRunConditional(async bool, f func() error) error {
	if async {
		go f()
		return nil
	} else {
		return f()
	}
}

func (p *ServiceContainer) changeStatus(s ServiceStatus) {
	p.mu.Lock()
	p.status = s
	p.mu.Unlock()
}

func (p *ServiceContainer) createContainer() (system.ContainerId, error) {
	if p.containerId != nil {
		return *p.containerId, nil
	}

	var err error

	p.containerConfig, p.containerMeta, err = p.fa.createContainerConfig()
	if err != nil {
		return "", fmt.Errorf("error while creating a container config: %#v)", err)
	}
	err = p.d.PullImage(p.containerConfig.Image)
	if err != nil {
		return "", fmt.Errorf("error while pulling image (ref: %#v): %#v)", p.containerConfig.Image, err)
	}

	containerId, err := p.d.CreateContainer(p.containerConfig)
	return containerId, err
}

func (p *ServiceContainer) isRunningState() bool {
	return p.status != Terminated && p.status != Stopped && p.status != Error
}

func (p *ServiceContainer) ContainerInfo() (system.CreateContainerOption, interface{}, bool) {
	p.mu.Lock()
	defer p.mu.Unlock()
	return p.containerConfig, p.containerMeta, p.containerId != nil
}

func (p *ServiceContainer) Start(ctx context.Context) error {
	async := GetAsync(ctx)
	err := func() error {
		p.mu.Lock()
		defer p.mu.Unlock()

		if p.isRunningState() {
			return errors.New("already started")
		}
		p.status = Starting
		return nil
	}()
	if err != nil {
		return err
	}

	return goRunConditional(async, func() error {
		err := func() error {
			cid, err := p.createContainer()
			if err != nil {
				return err
			}

			p.containerId = &cid
			return p.d.StartContainer(cid)
		}()
		if err != nil {
			p.changeStatus(Error)
		} else {
			p.changeStatus(Running)
		}
		return err
	})
}

func (p *ServiceContainer) getContainerId() (system.ContainerId, bool) {
	if p.containerId == nil {
		return "", false
	} else {
		return *p.containerId, true
	}
}

func (p *ServiceContainer) Stop(ctx context.Context) error {
	async := GetAsync(ctx)
	cid, err := func() (system.ContainerId, error) {
		p.mu.Lock()
		defer p.mu.Unlock()

		if p.status != Running {
			return "", errors.New("already stopped")
		}
		if cid, ok := p.getContainerId(); !ok {
			return "", errors.New("containerId is null")
		} else {
			p.status = Stopping
			return cid, nil
		}
	}()
	if err != nil {
		return err
	}

	return goRunConditional(async, func() error {
		timeout := 10 * time.Second
		err := p.d.StopContainer(cid, timeout)
		if err != nil {
			p.changeStatus(Error)
		} else {
			p.changeStatus(Stopped)
		}
		return err
	})
}

func (p *ServiceContainer) Terminate(ctx context.Context) error {
	async := GetAsync(ctx)
	cid, err := func() (system.ContainerId, error) {
		p.mu.Lock()
		defer p.mu.Unlock()

		if p.status != Terminated && p.status != Stopped {
			return "", errors.New("cannot clean running container")
		}

		cid, ok := p.getContainerId()
		if !ok {
			return "", errors.New("container already removed")
		}
		p.changeStatus(Terminated)
		p.containerId = nil
		return cid, nil
	}()
	if err != nil {
		return err
	}

	return goRunConditional(async, func() error {
		if err := p.d.RemoveContainer(cid); err != nil {
			return fmt.Errorf("got an error while removing the container: %#v, %#v", p.containerId, err)
		}
		return nil
	})
}

func (p *ServiceContainer) Status() ServiceStatus {
	return p.status
}

func (p *ServiceContainer) onCriticalSection(f func() interface{}) interface{} {
	p.mu.Lock()
	defer p.mu.Unlock()

	return f()
}
