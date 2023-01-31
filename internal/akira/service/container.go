package service

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"time"

	"github.com/AkariGroup/akari_software/internal/akira/system"
	CircBuffer "github.com/armon/circbuf"
	"github.com/rs/zerolog"
)

const LogBufferSize = 10000

type containerConfigFactory interface {
	createContainerConfig() (system.CreateContainerOption, interface{}, error)
}

type ServiceContainer struct {
	fa    containerConfigFactory
	d     *system.DockerSystem
	state ServiceState

	containerId     *system.ContainerId
	containerConfig system.CreateContainerOption
	containerMeta   interface{}

	logger    zerolog.Logger
	logBuffer *CircBuffer.Buffer

	mu sync.Mutex
}

func NewServiceContainer(fa containerConfigFactory, d *system.DockerSystem) *ServiceContainer {
	logBuffer, err := CircBuffer.NewBuffer(LogBufferSize)
	var logger zerolog.Logger
	if err != nil {
		logBuffer = nil
		logger = zerolog.Nop()
	} else {
		logger = zerolog.New(logBuffer).With().Timestamp().Logger()
	}

	return &ServiceContainer{
		fa:        fa,
		d:         d,
		state:     Terminated,
		logBuffer: logBuffer,
		logger:    logger,
	}
}

func validateStateChange(old ServiceState, new ServiceState) error {
	// State transition
	// Initial State := Terminated
	//
	// Terminated -> Starting | Error
	// Starting -> Running | Error
	// Running -> Stopping | Error
	// Stopping -> Stopped | Error
	// Stopped -> Terminated | Starting
	// Error -> Terminated

	switch new {
	case Terminated:
		if old != Stopped && old != Error {
			return errors.New("invalid transition")
		}
		return nil
	case Starting:
		if old != Terminated && old != Stopped {
			return errors.New("service already started")
		}
		return nil
	case Running:
		if old != Starting {
			return errors.New("invalid transition")
		}
		return nil
	case Stopping:
		if old != Running {
			return errors.New("invalid transition")
		}
		return nil
	case Stopped:
		if old != Stopping {
			return errors.New("invalid transition")
		}
		return nil
	case Error:
		return nil
	default:
		panic("invalid state")
	}
}

func (p *ServiceContainer) changeState(newState ServiceState) error {
	if err := validateStateChange(p.state, newState); err != nil {
		return err
	}
	p.state = newState
	return nil
}

func goRunConditional(async bool, f func() error) ServiceTask {
	if async {
		return runServiceTask(f)
	} else {
		err := f()
		return &serviceTask{
			err: err,
		}
	}
}

func (p *ServiceContainer) createContainer() (system.ContainerId, error) {
	var err error

	p.containerConfig, p.containerMeta, err = p.fa.createContainerConfig()
	if err != nil {
		return "", fmt.Errorf("error while creating a container config: %#v)", err)
	}
	err = p.d.PullImage(p.containerConfig.Image)
	if err != nil {
		// NOTE: Try launching service container if it fails to pull the latest docker image (e.g. no network connection)
		p.logger.Warn().Msgf("failed to pull image (ref: %#v): %#v)", p.containerConfig.Image, err)
	}

	containerId, err := p.d.CreateContainer(p.containerConfig)
	return containerId, err
}

func (p *ServiceContainer) ContainerInfo() (system.CreateContainerOption, interface{}, bool) {
	p.mu.Lock()
	defer p.mu.Unlock()
	return p.containerConfig, p.containerMeta, p.containerId != nil
}

func (p *ServiceContainer) Start(ctx context.Context) (ret ServiceTask, err error) {
	ret = &serviceTask{}

	p.mu.Lock()
	err = p.changeState(Starting)
	cid := p.containerId
	p.mu.Unlock()

	if err != nil {
		return
	}

	async := GetAsync(ctx)
	ret = goRunConditional(async, func() (err error) {
		var containerId system.ContainerId

		if cid != nil {
			containerId = *cid
		} else {
			containerId, err = p.createContainer()
			if err != nil {
				return
			}

			p.mu.Lock()
			p.containerId = &containerId
			p.mu.Unlock()
		}

		err = p.d.StartContainer(containerId)
		if err != nil {
			return
		}

		p.mu.Lock()
		if err != nil {
			p.changeState(Error)
		} else {
			p.changeState(Running)
		}
		p.mu.Unlock()
		return
	})
	return
}

func (p *ServiceContainer) Stop(ctx context.Context) (ret ServiceTask, err error) {
	ret = &serviceTask{}

	p.mu.Lock()
	err = p.changeState(Stopping)
	cid := p.containerId
	p.mu.Unlock()

	if err != nil || cid == nil {
		return
	}

	async := GetAsync(ctx)
	ret = goRunConditional(async, func() error {
		timeout := 10 * time.Second
		err := p.d.StopContainer(*cid, timeout)

		p.mu.Lock()
		defer p.mu.Unlock()
		if err != nil {
			p.changeState(Error)
		} else {
			p.changeState(Stopped)
		}
		return err
	})
	return
}

func (p *ServiceContainer) Terminate(ctx context.Context) (ret ServiceTask, err error) {
	ret = &serviceTask{}

	p.mu.Lock()
	cid := p.containerId
	err = p.changeState(Terminated)
	if err == nil {
		p.containerId = nil
	}
	p.mu.Unlock()

	if err != nil || cid == nil {
		return
	}

	async := GetAsync(ctx)
	ret = goRunConditional(async, func() error {
		if err := p.d.RemoveContainer(*cid); err != nil {
			return fmt.Errorf("got an error while removing the container: %#v, %#v", p.containerId, err)
		}
		return nil
	})
	return
}

func (p *ServiceContainer) State() ServiceState {
	return p.state
}

func (p *ServiceContainer) Logs() string {
	if p.logBuffer == nil {
		return ""
	}

	return p.logBuffer.String()
}

func (p *ServiceContainer) CheckAlive() error {
	p.mu.Lock()
	defer p.mu.Unlock()

	if p.state != Running {
		return nil
	}

	cid := p.containerId
	if cid == nil {
		return nil
	}

	if !p.d.CheckContainerRunning(*cid) {
		p.changeState(Error)
	}
	return nil
}
