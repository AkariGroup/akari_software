package service

import (
	"os"
	"path/filepath"
	"sync"

	"github.com/go-playground/validator/v10"
	yaml "github.com/goccy/go-yaml"
)

type ServiceAutoStartConfig struct {
	Services map[ServiceId]bool `json:"services" validate:"required"`
}

type ServiceAutoStartManager struct {
	config     ServiceAutoStartConfig
	configPath string

	mu sync.Mutex
}

func NewServiceAutoStartManager(configPath string) *ServiceAutoStartManager {
	return &ServiceAutoStartManager{
		config: ServiceAutoStartConfig{
			Services: make(map[ServiceId]bool),
		},
		configPath: configPath,
	}
}

func (m *ServiceAutoStartManager) LoadConfig() error {
	m.mu.Lock()
	defer m.mu.Unlock()

	content, err := os.ReadFile(m.configPath)
	if err != nil {
		// NOTE: Do nothing if config file is missing
		if os.IsNotExist(err) {
			return nil
		}
		return err
	}

	v := validator.New()
	if err = yaml.UnmarshalWithOptions(
		content,
		&m.config,
		yaml.Strict(),
		yaml.Validator(v),
	); err != nil {
		return err
	}
	return nil
}

func (m *ServiceAutoStartManager) SaveConfig() error {
	m.mu.Lock()
	defer m.mu.Unlock()

	content, err := yaml.Marshal(m.config)
	if err != nil {
		return err
	}

	dir := filepath.Dir(m.configPath)
	if err := os.MkdirAll(dir, os.ModePerm); err != nil {
		return err
	}

	fs, err := os.Create(m.configPath)
	if err != nil {
		return err
	}

	fs.Write(content)
	fs.Close()
	return nil
}

func (m *ServiceAutoStartManager) Cleanup(services map[ServiceId]interface{}) {
	m.mu.Lock()
	defer m.mu.Unlock()

	for s, _ := range m.config.Services {
		_, ok := services[s]
		if !ok {
			delete(m.config.Services, s)
		}
	}
}

func (m *ServiceAutoStartManager) GetEnabled(id ServiceId) bool {
	m.mu.Lock()
	defer m.mu.Unlock()

	// NOTE: config.Services might contains false values if the config file is edited manually
	v, autoStart := m.config.Services[id]
	return v && autoStart
}

func (m *ServiceAutoStartManager) SetEnabled(id ServiceId, enabled bool) {
	m.mu.Lock()
	defer m.mu.Unlock()

	if enabled {
		m.config.Services[id] = true
	} else {
		delete(m.config.Services, id)
	}
}
