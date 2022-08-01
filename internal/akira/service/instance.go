package service

import (
	"io/ioutil"
	"os"
	"path/filepath"

	"github.com/go-playground/validator/v10"
	yaml "github.com/goccy/go-yaml"
	"github.com/google/uuid"
)

type InstanceId string
type InstanceStatus int8

const (
	Terminated InstanceStatus = iota
	Starting
	Running
	Stopping
	Error
	Stopped
)

func NewInstanceId() InstanceId {
	return InstanceId(uuid.New().String())
}

type InstanceConfig struct {
	Id        InstanceId `json:"id" validate:"required"`
	ServiceId ServiceId  `json:"service_id" validate:"required"`

	DisplayName string `json:"display_name" validate:"required"`
	Description string `json:"description"`
}

type Instance interface {
	Id() InstanceId
	Config() InstanceConfig

	Start() error
	Stop() error
	Terminate() error
	Clean() error
	Status() InstanceStatus

	GetOpenAddress() (string, error)
	GetOpenProjectAddress(projectDir string) (string, error)
}

func loadInstanceConfig(p string) (InstanceConfig, error) {
	content, err := ioutil.ReadFile(p)
	if err != nil {
		return InstanceConfig{}, err
	}

	v := validator.New()
	var config InstanceConfig
	err = yaml.UnmarshalWithOptions(
		content,
		&config,
		yaml.Strict(),
		yaml.Validator(v),
	)
	return config, err
}

func saveInstanceConfig(c InstanceConfig, p string) error {
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
