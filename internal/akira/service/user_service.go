package service

import (
	"errors"
	"os"
	"path/filepath"
)

type UserServiceProvider struct {
	image ImageConfig
	opts  ServiceManagerOptions

	*ServiceContainer
	*ServiceConfigAccessor
	*ServiceConfigLoader
}

func NewUserServiceProvider(
	fa containerConfigFactory,
	config ServiceConfig,
	configPath string,
	image ImageConfig,
	opts ServiceManagerOptions,
) *UserServiceProvider {
	p := &UserServiceProvider{
		image: image,
		opts:  opts,

		ServiceContainer: NewServiceContainer(fa, opts.Docker),
	}
	p.ServiceConfigAccessor = &ServiceConfigAccessor{config: config}
	p.ServiceConfigLoader = &ServiceConfigLoader{&p.ServiceConfigAccessor.config, configPath}
	return p
}

func (p *UserServiceProvider) varDir() string {
	return filepath.Join(p.opts.ServiceVarDir, string(p.ServiceConfigAccessor.Id()))
}

func (p *UserServiceProvider) Type() ServiceType {
	return ServiceTypeUser
}

func (p *UserServiceProvider) Capabilities() []ServiceCapability {
	return p.image.Capabilities
}

func (p *UserServiceProvider) Clean() error {
	ret := p.ServiceContainer.onCriticalSection(func() interface{} {
		if p.ServiceContainer.Status() != Terminated {
			return errors.New("cannot remove directory of existing container")
		}

		return os.RemoveAll(p.varDir())
	})
	if err, ok := ret.(error); ok {
		return err
	}
	return nil
}

func (p *UserServiceProvider) SetConfig(c ServiceConfig) error {
	p.ServiceConfigAccessor.config = c
	return nil
}
