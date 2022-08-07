package service

import (
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
	id     ServiceId
	fa     containerConfigFactory
	d      *system.DockerSystem
	status ServiceStatus

	containerId     *system.ContainerId
	containerConfig system.CreateContainerOption
	containerMeta   interface{}

	mu sync.Mutex
}

func NewServiceContainer(id ServiceId, fa containerConfigFactory, d *system.DockerSystem) *ServiceContainer {
	return &ServiceContainer{
		id:     id,
		fa:     fa,
		d:      d,
		status: Terminated,
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

func (p *ServiceContainer) Start() error {
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

	err = func() error {
		cid, err := p.createContainer()
		if err != nil {
			return err
		}

		p.containerId = &cid
		return p.d.StartContainer(cid)
	}()
	if err != nil {
		p.changeStatus(Error)
		return err
	}

	p.changeStatus(Running)
	return nil
}

func (p *ServiceContainer) getContainerId() (system.ContainerId, bool) {
	if p.containerId == nil {
		return "", false
	} else {
		return *p.containerId, true
	}
}

func (p *ServiceContainer) Stop() error {
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

	timeout := 10 * time.Second
	if err := p.d.StopContainer(cid, timeout); err != nil {
		p.changeStatus(Error)
		return err
	} else {
		p.changeStatus(Stopped)
		return nil
	}
}

func (p *ServiceContainer) Terminate() error {
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
		p.containerId = nil
		return cid, nil
	}()
	if err != nil {
		return err
	}
	p.changeStatus(Terminated)
	if err := p.d.RemoveContainer(cid); err != nil {
		return fmt.Errorf("got an error while removing the container: %#v, %#v", p.containerId, err)
	}
	return nil
}

func (p *ServiceContainer) Status() ServiceStatus {
	return p.status
}

func (p *ServiceContainer) onCriticalSection(f func() interface{}) interface{} {
	p.mu.Lock()
	defer p.mu.Unlock()

	return f()
}
