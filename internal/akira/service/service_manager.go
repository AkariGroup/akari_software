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
	Instances() []Instance

	GetImage(s ImageId) (ImageConfig, bool)

	CreateInstance(s ImageId, displayName string, description string) (Instance, error)
	GetInstance(s InstanceId) (Instance, bool)
	RemoveInstance(s InstanceId) error
}

type ServiceManagerOptions struct {
	ServiceDir        string
	InstanceConfigDir string
	InstanceVarDir    string
	ProjectRootDir    string
	Docker            *system.DockerSystem
}

type serviceManager struct {
	images    map[ImageId]ImageConfig
	instances map[InstanceId]Instance
	opts      ServiceManagerOptions

	mu sync.RWMutex
}

func NewServiceManager(opts ServiceManagerOptions) (ServiceManager, error) {
	var err error
	if opts.ProjectRootDir, err = filepath.Abs(opts.ProjectRootDir); err != nil {
		return nil, err
	}
	if opts.InstanceConfigDir, err = filepath.Abs(opts.InstanceConfigDir); err != nil {
		return nil, err
	}
	if opts.InstanceVarDir, err = filepath.Abs(opts.InstanceVarDir); err != nil {
		return nil, err
	}

	m := &serviceManager{
		images:    make(map[ImageId]ImageConfig),
		instances: make(map[InstanceId]Instance),
		opts:      opts,
	}
	if err := m.scanImages(); err != nil {
		return nil, err
	}
	if err := m.scanInstances(); err != nil {
		return nil, err
	}
	return m, nil
}

func (m *serviceManager) scanImages() error {
	// TODO: Load Image from directory
	jupyterId := ImageId("bca6daa4-b41f-4729-bac3-34f161f9ad91")
	m.images[jupyterId] = ImageConfig{
		Id:          jupyterId,
		Name:        JupyterLabServiceName,
		Version:     "v1",
		DisplayName: "JupyterLab",
		Description: "Launch a jupyter lab",
		Capabilities: []ServiceCapability{
			CapabilityOpen,
			CapabilityOpenProject,
		},
		ContainerOption: ServiceContainerOption{
			Image: "docker.io/akarirobot/akira-jupyter-service",
		},
	}
	return nil
}

func (m *serviceManager) loadInstance(c InstanceConfig) (Instance, error) {
	s, ok := m.images[c.ImageId]
	if !ok {
		return nil, fmt.Errorf("service id: %#v not found", c.ImageId)
	}

	switch s.Name {
	case JupyterLabServiceName:
		instance := NewJupyterLab(s, c, m.opts)
		return instance, nil
	default:
		return nil, fmt.Errorf("unsupported service name: %#v", s.Name)
	}
}

func (m *serviceManager) scanInstances() error {
	files, err := ioutil.ReadDir(m.opts.InstanceConfigDir)
	if err != nil {
		return fmt.Errorf("error while scanning instances: %#v\n", err)
	}

	for _, f := range files {
		if f.IsDir() {
			continue
		}
		p := filepath.Join(m.opts.InstanceConfigDir, f.Name())
		base := filepath.Base(p)
		if strings.HasPrefix(base, ".") || !strings.HasSuffix(p, ".yaml") {
			continue
		}

		config, err := loadInstanceConfig(p)
		if err != nil {
			log.Printf("error while loading metadata: %#v\n", err)
			continue
		}
		instance, err := m.loadInstance(config)
		if err != nil {
			log.Printf("failed to load instance: %#v\n", err)
			continue
		} else {
			m.instances[config.Id] = instance
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

func (m *serviceManager) Instances() []Instance {
	m.mu.RLock()
	defer m.mu.RUnlock()

	var ret []Instance
	for _, v := range m.instances {
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

func (m *serviceManager) CreateInstance(s ImageId, displayName string, description string) (Instance, error) {
	m.mu.Lock()
	defer m.mu.Unlock()

	_, ok := m.images[s]
	if !ok {
		return nil, fmt.Errorf("service: %s doesn't exist", s)
	}

	config := InstanceConfig{
		Id:          NewInstanceId(),
		ImageId:     s,
		DisplayName: displayName,
		Description: description,
	}
	if err := saveInstanceConfig(
		config,
		filepath.Join(m.opts.InstanceConfigDir, fmt.Sprintf("%s.yaml", string(config.Id))),
	); err != nil {
		return nil, fmt.Errorf("failed to save instance config: %#v", err)
	}
	instance, err := m.loadInstance(config)
	if err != nil {
		return nil, fmt.Errorf("failed to load instance: %#v", err)
	}
	m.instances[config.Id] = instance
	return instance, nil
}

func (m *serviceManager) GetInstance(id InstanceId) (Instance, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	s, ok := m.instances[id]
	return s, ok
}

func (m *serviceManager) RemoveInstance(id InstanceId) error {
	s, ok := m.GetInstance(id)
	if !ok {
		return fmt.Errorf("instance doesn't exist: %#v", id)
	}

	s.Stop()
	s.Terminate()
	s.Clean()

	m.mu.Lock()
	delete(m.instances, id)
	m.mu.Unlock()

	p := filepath.Join(m.opts.InstanceConfigDir, fmt.Sprintf("%s.yaml", string(s.Id())))
	os.Remove(p)
	return nil
}
