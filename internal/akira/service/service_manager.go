package service

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
	"sync"

	"github.com/AkariGroup/akari_software/internal/akira/system"
)

type ServiceManager interface {
	Images() []ImageConfig
	Services() []Service

	GetImage(s ImageId) (ImageConfig, bool)

	CreateUserService(s ImageId, displayName string, description string) (Service, error)
	GetService(s ServiceId) (Service, bool)
	RemoveUserService(s ServiceId) error
}

type ServiceManagerOptions struct {
	ImageConfigDir   string
	ServiceConfigDir string
	ServiceVarDir    string
	EtcDir           string
	ProjectRootDir   string
	Docker           *system.DockerSystem
}

type serviceManager struct {
	images   map[ImageId]ImageConfig
	services map[ServiceId]Service
	opts     ServiceManagerOptions

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
	}
	if err := m.scanImages(); err != nil {
		return nil, err
	}
	if err := m.scanServices(); err != nil {
		return nil, err
	}
	return m, nil
}

func (m *serviceManager) scanImages() error {
	// TODO: Load Image from directory
	img := jupyterLabImageConfig()
	m.images[img.Id] = img
	return nil
}

func (m *serviceManager) loadService(c ServiceConfig) (Service, error) {
	s, ok := m.images[c.ImageId]
	if !ok {
		return nil, fmt.Errorf("service id: %#v not found", c.ImageId)
	}

	switch s.Name {
	case JupyterLabServiceName:
		service := NewJupyterLab(s, c, m.opts)
		return service, nil
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
		return fmt.Errorf("error while scanning services: %#v\n", err)
	}

	// TODO: scan system services
	if rpcServerConfig, err := akariRpcServerSystemServiceConfig(m.opts.EtcDir); err != nil {
		log.Printf("error while initializing rpc server: %#v\n", err)
	} else {
		registerService(
			NewSystemService(rpcServerConfig, m.opts),
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

		config, err := loadServiceConfig(p)
		if err != nil {
			log.Printf("error while loading metadata: %#v\n", err)
			continue
		}
		service, err := m.loadService(config)
		if err != nil {
			log.Printf("failed to load service: %#v\n", err)
			continue
		} else {
			registerService(service)
		}
	}

	return nil
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
	if err := saveServiceConfig(
		config,
		filepath.Join(m.opts.ServiceConfigDir, fmt.Sprintf("%s.yaml", string(config.Id))),
	); err != nil {
		return nil, fmt.Errorf("failed to save service config: %#v", err)
	}
	// We suppose that loadService only returns a UserService
	service, err := m.loadService(config)
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

	s.Stop()
	s.Terminate()
	s.Clean()

	m.mu.Lock()
	delete(m.services, id)
	m.mu.Unlock()

	p := filepath.Join(m.opts.ServiceConfigDir, fmt.Sprintf("%s.yaml", string(s.Id())))
	os.Remove(p)
	return nil
}
