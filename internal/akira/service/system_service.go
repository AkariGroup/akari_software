package service

import (
	"errors"
	"github.com/AkariGroup/akari_software/internal/akira/system"
)

type SystemServiceConfig struct {
	Id              ServiceId                    `json:"id" validate:"required"`
	DisplayName     string                       `json:"display_name" validate:"required"`
	Description     string                       `json:"description"`
	ContainerOption system.CreateContainerOption `json:"container_option" validate:"required"`
}

type SystemService struct {
	config    SystemServiceConfig
	opts      ServiceManagerOptions
	container *ServiceContainer
}

func NewSystemService(config SystemServiceConfig, opts ServiceManagerOptions) *SystemService {
	p := &SystemService{
		config: config,
		opts:   opts,
	}
	p.container = NewServiceContainer(p, opts.Docker)
	return p
}

func (p *SystemService) Id() ServiceId {
	return p.config.Id
}

func (p *SystemService) DisplayName() string {
	return p.config.DisplayName
}

func (p *SystemService) Description() string {
	return p.config.Description
}

func (p *SystemService) ImageId() ImageId {
	return NullImageId
}

func (p *SystemService) Type() ServiceType {
	return ServiceTypeSystem
}

func (p *SystemService) Capabilities() []ServiceCapability {
	return nil
}

func (p *SystemService) createContainerConfig() (system.CreateContainerOption, interface{}, error) {
	return p.config.ContainerOption, nil, nil
}

func (p *SystemService) Start() error {
	return p.container.Start()
}

func (p *SystemService) Stop() error {
	return p.container.Stop()
}

func (p *SystemService) Terminate() error {
	return p.container.Terminate()
}

func (p *SystemService) Clean() error {
	return nil
}

func (p *SystemService) Status() ServiceStatus {
	return p.container.Status()
}

func (p *SystemService) GetOpenAddress(hostName string) (string, error) {
	return "", errors.New("unsupported operation")
}

func (p *SystemService) GetOpenProjectAddress(hostName string, projectDir string) (string, error) {
	return "", errors.New("unsupported operation")
}
