package service

import (
	"io/ioutil"
	"os"
	"path/filepath"

	"github.com/go-playground/validator/v10"
	yaml "github.com/goccy/go-yaml"
)

type ServiceConfig struct {
	Id          ServiceId `json:"id" validate:"required"`
	ImageId     ImageId   `json:"image_id" validate:"required"`
	DisplayName string    `json:"display_name" validate:"required"`
	Description string    `json:"description"`
	AutoStart   bool      `json:"auto_start"`
}

type ServiceConfigAccessor struct {
	config ServiceConfig
}

func (g *ServiceConfigAccessor) Id() ServiceId {
	return g.config.Id
}

func (g *ServiceConfigAccessor) Config() ServiceConfig {
	return g.config
}

type ServiceConfigLoader struct {
	config     *ServiceConfig
	configPath string
}

func (w *ServiceConfigLoader) LoadConfig() error {
	content, err := ioutil.ReadFile(w.configPath)
	if err != nil {
		return err
	}

	v := validator.New()
	if err = yaml.UnmarshalWithOptions(
		content,
		w.config,
		yaml.Strict(),
		yaml.Validator(v),
	); err != nil {
		return err
	}
	return nil
}

func (w *ServiceConfigLoader) SaveConfig() error {
	content, err := yaml.Marshal(w.config)
	if err != nil {
		return err
	}

	dir := filepath.Dir(w.configPath)
	if err := os.MkdirAll(dir, os.ModePerm); err != nil {
		return err
	}

	fs, err := os.Create(w.configPath)
	if err != nil {
		return err
	}

	fs.Write(content)
	fs.Close()
	return nil
}
