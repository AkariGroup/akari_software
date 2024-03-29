package service

import (
	"context"
	"errors"
	"fmt"
	"strings"
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

func createLogWriter(buf *CircBuffer.Buffer) zerolog.ConsoleWriter {
	output := zerolog.ConsoleWriter{Out: buf, TimeFormat: time.RFC3339, NoColor: true}
	output.FormatLevel = func(i interface{}) string {
		return strings.ToUpper(fmt.Sprintf("|%6s|", i))
	}
	output.FormatMessage = func(i interface{}) string {
		return fmt.Sprintf("%s", i)
	}
	output.FormatFieldName = func(i interface{}) string {
		return fmt.Sprintf("%s:", i)
	}
	output.FormatFieldValue = func(i interface{}) string {
		return strings.ToUpper(fmt.Sprintf("%s", i))
	}

	return output
}

func NewServiceContainer(fa containerConfigFactory, d *system.DockerSystem) *ServiceContainer {
	logBuffer, err := CircBuffer.NewBuffer(LogBufferSize)
	var logger zerolog.Logger
	if err != nil {
		logBuffer = nil
		logger = zerolog.Nop()
	} else {
		logger = zerolog.New(createLogWriter(logBuffer)).With().Timestamp().Logger()
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
	p.logger.Info().Msgf("changing state from %v to %v", p.state, newState)
	if err := validateStateChange(p.state, newState); err != nil {
		p.logger.Err(err).Msgf("failed to change state")
		return err
	}
	p.state = newState
	p.logger.Info().Msgf("state has changed to %v", newState)
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
		p.logger.Warn().Msgf("failed to pull image (ref: %#s): %#s", p.containerConfig.Image, err)
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
		p.logger.Err(err).Msg("failed to start service")
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
				p.logger.Err(err).Msg("failed to create container")
				return
			}

			p.mu.Lock()
			p.containerId = &containerId
			p.mu.Unlock()
		}

		err = p.d.StartContainer(containerId)
		p.mu.Lock()
		if err != nil {
			p.logger.Err(err).Msg("failed to start container")
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
		p.logger.Error().Msg("failed to stop service")
		return
	}

	async := GetAsync(ctx)
	ret = goRunConditional(async, func() error {
		timeout := 10 * time.Second
		err := p.d.StopContainer(*cid, timeout)

		p.mu.Lock()
		defer p.mu.Unlock()
		if err != nil {
			p.logger.Err(err).Msg("failed to stop container")
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
		p.logger.Warn().Msg("failed to terminate service")
		return
	}

	async := GetAsync(ctx)
	ret = goRunConditional(async, func() error {
		if err := p.d.RemoveContainer(*cid); err != nil {
			p.logger.Err(err).Msg("failed to remove container")
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

func (p *ServiceContainer) Outputs() (string, string) {
	p.mu.Lock()
	cid := p.containerId
	p.mu.Unlock()

	if cid == nil {
		return "", ""
	}

	stdout, stderr, err := p.d.GetContainerOutputs(*cid)
	if err != nil {
		p.logger.Err(err).Msg("failed to get container output")
		return "", ""
	}

	return stdout, stderr
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
