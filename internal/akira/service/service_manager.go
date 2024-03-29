package service

import (
	"context"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/AkariGroup/akari_software/internal/akira/system"
	"github.com/rs/zerolog/log"
)

const (
	CheckAlivePeriodSeconds = 10
)

type ServiceManager interface {
	Images() []ImageConfig
	Services() []Service

	GetImage(s ImageId) (ImageConfig, bool)

	CreateUserService(s ImageId, displayName string, description string) (Service, error)
	GetService(s ServiceId) (Service, bool)
	RemoveUserService(s ServiceId) error

	SetServiceAutoStartEnabled(id ServiceId, enabled bool) error
	GetServiceAutoStartEnabled(id ServiceId) (bool, error)
}

type ServiceManagerOptions struct {
	ImageConfigDir          string
	ServiceConfigDir        string
	ServiceManagerConfigDir string
	ServiceVarDir           string
	EtcDir                  string
	ProjectRootDir          string
	Docker                  *system.DockerSystem
}

type serviceManager struct {
	images    map[ImageId]ImageConfig
	services  map[ServiceId]Service
	autoStart *ServiceAutoStartManager

	opts ServiceManagerOptions

	mu sync.RWMutex
}

func NewServiceManager(opts ServiceManagerOptions) (ServiceManager, error) {
	var err error
	if opts.ProjectRootDir, err = filepath.Abs(opts.ProjectRootDir); err != nil {
		return nil, err
	}
	if opts.ServiceConfigDir, err = filepath.Abs(opts.ServiceConfigDir); err != nil {
		return nil, err
	}
	if opts.ServiceVarDir, err = filepath.Abs(opts.ServiceVarDir); err != nil {
		return nil, err
	}

	m := &serviceManager{
		images:   make(map[ImageId]ImageConfig),
		services: make(map[ServiceId]Service),
		opts:     opts,
		autoStart: NewServiceAutoStartManager(
			filepath.Join(opts.ServiceManagerConfigDir, "auto_start.yaml"),
		),
	}
	if err := m.scanImages(); err != nil {
		return nil, err
	}
	if err := m.scanServices(); err != nil {
		return nil, err
	}
	if err := m.initializeAutoStartServices(); err != nil {
		return nil, err
	}

	// Run CheckAlive() periodically
	go func() {
		for {
			m.CheckAlive()
			time.Sleep(CheckAlivePeriodSeconds * time.Second)
		}
	}()

	return m, nil
}

func (m *serviceManager) initializeAutoStartServices() error {
	m.mu.Lock()
	defer m.mu.Unlock()

	if err := m.autoStart.LoadConfig(); err != nil {
		return err
	}
	sids := make(map[ServiceId]interface{})
	for s, _ := range m.services {
		sids[s] = struct{}{}
	}
	m.autoStart.Cleanup(sids)

	ctx := SetAsync(context.Background(), true)
	for sid, s := range m.services {
		if !m.autoStart.GetEnabled(sid) {
			continue
		}
		s.Start(ctx)
	}

	return nil
}

func (m *serviceManager) scanImages() error {
	// TODO: Load Image from directory
	img := jupyterLabImageConfig()
	m.images[img.Id] = img

	img = vscodeImageConfig()
	m.images[img.Id] = img
	return nil
}

func (m *serviceManager) loadUserService(path string) (UserService, error) {
	var config ServiceConfig
	loader := ServiceConfigLoader{
		config:     &config,
		configPath: path,
	}
	if err := loader.LoadConfig(); err != nil {
		log.Warn().Msgf("error while loading metadata: %#v", err)
		return nil, err
	}

	s, ok := m.images[config.ImageId]
	if !ok {
		return nil, fmt.Errorf("service id: %#v not found", config.ImageId)
	}

	switch s.Name {
	case JupyterLabServiceName:
		return NewJupyterLab(s, config, path, m.opts), nil
	case VSCodeServiceName:
		return NewVSCode(s, config, path, m.opts), nil
	default:
		return nil, fmt.Errorf("unsupported service name: %#v", s.Name)
	}
}

func (m *serviceManager) scanServices() error {
	registerService := func(s Service) {
		m.services[s.Id()] = s
	}

	files, err := ioutil.ReadDir(m.opts.ServiceConfigDir)
	if err != nil {
		return fmt.Errorf("error while scanning services: %#v", err)
	}

	// TODO: scan system services
	if config, containerOpts, err := akariRpcServerSystemServiceConfig(m.opts.EtcDir); err != nil {
		log.Error().Msgf("error while initializing rpc server: %#v", err)
	} else {
		registerService(
			NewSystemService(config, containerOpts, m.opts),
		)
	}

	if config, containerOpts, err := akiraControllerServerServiceConfig(m.opts.EtcDir); err != nil {
		log.Error().Msgf("error while initializing controller server: %#v", err)
	} else {
		registerService(
			NewSystemService(config, containerOpts, m.opts),
		)
	}

	for _, f := range files {
		if f.IsDir() {
			continue
		}
		p := filepath.Join(m.opts.ServiceConfigDir, f.Name())
		base := filepath.Base(p)
		if strings.HasPrefix(base, ".") || !strings.HasSuffix(p, ".yaml") {
			continue
		}

		if service, err := m.loadUserService(p); err != nil {
			log.Warn().Msgf("failed to load service: %#v", err)
			continue
		} else {
			registerService(service)
		}
	}

	return nil
}

func (m *serviceManager) CheckAlive() {
	m.mu.RLock()
	defer m.mu.RUnlock()

	for _, s := range m.services {
		s.CheckAlive()
	}
}

func (m *serviceManager) Images() []ImageConfig {
	m.mu.RLock()
	defer m.mu.RUnlock()

	var ret []ImageConfig
	for _, v := range m.images {
		ret = append(ret, v)
	}
	return ret
}

func (m *serviceManager) Services() []Service {
	m.mu.RLock()
	defer m.mu.RUnlock()

	var ret []Service
	for _, v := range m.services {
		ret = append(ret, v)
	}
	return ret
}

func (m *serviceManager) GetImage(s ImageId) (ImageConfig, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	sv, ok := m.images[s]
	return sv, ok
}

func (m *serviceManager) CreateUserService(s ImageId, displayName string, description string) (Service, error) {
	m.mu.Lock()
	defer m.mu.Unlock()

	_, ok := m.images[s]
	if !ok {
		return nil, fmt.Errorf("service: %s doesn't exist", s)
	}

	config := ServiceConfig{
		Id:          NewServiceId(),
		ImageId:     s,
		DisplayName: displayName,
		Description: description,
	}
	configPath := filepath.Join(m.opts.ServiceConfigDir, fmt.Sprintf("%s.yaml", string(config.Id)))
	writer := ServiceConfigLoader{
		config:     &config,
		configPath: configPath,
	}
	if err := writer.SaveConfig(); err != nil {
		return nil, fmt.Errorf("failed to save service config: %#v", err)
	}
	service, err := m.loadUserService(configPath)
	if err != nil {
		return nil, fmt.Errorf("failed to load service: %#v", err)
	}
	m.services[config.Id] = service
	return service, nil
}

func (m *serviceManager) GetService(id ServiceId) (Service, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	s, ok := m.services[id]
	return s, ok
}

func (m *serviceManager) RemoveUserService(id ServiceId) error {
	s, ok := m.GetService(id)
	if !ok {
		return fmt.Errorf("service doesn't exist: %#v", id)
	}
	if s.Type() != ServiceTypeUser {
		return fmt.Errorf("cannot remove non-user service: %#v", id)
	}

	ctx := context.Background()
	s.Stop(ctx)
	s.Terminate(ctx)

	s.Clean()

	m.mu.Lock()
	delete(m.services, id)
	m.mu.Unlock()

	p := filepath.Join(m.opts.ServiceConfigDir, fmt.Sprintf("%s.yaml", string(s.Id())))
	os.Remove(p)
	return nil
}

func (m *serviceManager) serviceExists(id ServiceId) bool {
	_, ok := m.services[id]
	return ok
}

func (m *serviceManager) GetServiceAutoStartEnabled(id ServiceId) (bool, error) {
	m.mu.Lock()
	defer m.mu.Unlock()

	if !m.serviceExists(id) {
		return false, fmt.Errorf("service doesn't exist: %#v", id)
	}
	return m.autoStart.GetEnabled(id), nil
}

func (m *serviceManager) SetServiceAutoStartEnabled(id ServiceId, enabled bool) error {
	m.mu.Lock()
	defer m.mu.Unlock()

	if !m.serviceExists(id) {
		return fmt.Errorf("service doesn't exist: %#v", id)
	}
	m.autoStart.SetEnabled(id, enabled)
	return m.autoStart.SaveConfig()
}
