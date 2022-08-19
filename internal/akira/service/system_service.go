package service

import (
	"errors"

	"github.com/AkariGroup/akari_software/internal/akira/system"
)

type SystemService struct {
	opts          ServiceManagerOptions
	containerOpts system.CreateContainerOption

	*ServiceContainer
	*ServiceConfigAccessor
}

func NewSystemService(config ServiceConfig, containerOpts system.CreateContainerOption, opts ServiceManagerOptions) *SystemService {
	p := &SystemService{
		opts:          opts,
		containerOpts: containerOpts,

		ServiceConfigAccessor: &ServiceConfigAccessor{config},
	}
	p.ServiceContainer = NewServiceContainer(p, opts.Docker)
	return p
}

func (p *SystemService) Type() ServiceType {
	return ServiceTypeSystem
}

func (p *SystemService) Capabilities() []ServiceCapability {
	return nil
}

func (p *SystemService) createContainerConfig() (system.CreateContainerOption, interface{}, error) {
	return p.containerOpts, nil, nil
}

func (p *SystemService) Clean() error {
	return nil
}

func (p *SystemService) GetOpenAddress(hostName string) (string, error) {
	return "", errors.New("unsupported operation")
}

func (p *SystemService) GetOpenProjectAddress(hostName string, projectDir string) (string, error) {
	return "", errors.New("unsupported operation")
}
