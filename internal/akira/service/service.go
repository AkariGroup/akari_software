package service

import (
	"io/ioutil"
	"os"
	"path/filepath"

	"github.com/go-playground/validator/v10"
	yaml "github.com/goccy/go-yaml"
	"github.com/google/uuid"
)

type ServiceId string
type ServiceStatus int8
type ServiceType int8
type ServiceCapability string

const (
	CapabilityOpen        ServiceCapability = "open"
	CapabilityOpenProject                   = "open_project"
)

const (
	Terminated ServiceStatus = iota
	Starting
	Running
	Stopping
	Error
	Stopped
)

const (
	ServiceTypeUser ServiceType = iota
	ServiceTypeSystem
)

func NewServiceId() ServiceId {
	return ServiceId(uuid.New().String())
}

type ServiceConfig struct {
	Id      ServiceId `json:"id" validate:"required"`
	ImageId ImageId   `json:"image_id" validate:"required"`

	DisplayName string `json:"display_name" validate:"required"`
	Description string `json:"description"`
}

type Service interface {
	Id() ServiceId
	DisplayName() string
	Description() string
	ImageId() ImageId
	Type() ServiceType
	Capabilities() []ServiceCapability

	Start() error
	Stop() error
	Terminate() error
	Clean() error
	Status() ServiceStatus

	GetOpenAddress(hostName string) (string, error)
	GetOpenProjectAddress(hostName string, projectDir string) (string, error)
}

func loadServiceConfig(p string) (ServiceConfig, error) {
	content, err := ioutil.ReadFile(p)
	if err != nil {
		return ServiceConfig{}, err
	}

	v := validator.New()
	var config ServiceConfig
	err = yaml.UnmarshalWithOptions(
		content,
		&config,
		yaml.Strict(),
		yaml.Validator(v),
	)
	return config, err
}

func saveServiceConfig(c ServiceConfig, p string) error {
	content, err := yaml.Marshal(c)
	if err != nil {
		return err
	}

	dir := filepath.Dir(p)
	if err := os.MkdirAll(dir, os.ModePerm); err != nil {
		return err
	}

	fs, err := os.Create(p)
	if err != nil {
		return err
	}

	fs.Write(content)
	fs.Close()
	return nil
}
