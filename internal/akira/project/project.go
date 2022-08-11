package project

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"

	"github.com/go-playground/validator/v10"
	yaml "github.com/goccy/go-yaml"

	"github.com/AkariGroup/akari_software/internal/akira/internal/util"
)

type ProjectId = string

const ManifestFileName = "akari_manifest.yaml"

type ProjectManifest struct {
	Name        string `json:"name" validate:"required"`
	Description string `json:"description"`
	Author      string `json:"author"`
	Url         string `json:"url"`
}

type Project interface {
	Id() ProjectId
	Manifest() ProjectManifest
	Path() string

	LoadManifest() error
	SaveManifest() error
}

type localProject struct {
	manifest     ProjectManifest
	manifestPath string
}

func (p *localProject) Id() ProjectId {
	return p.Path()
}

func (p *localProject) Name() string {
	return p.manifest.Name
}

func (p *localProject) Manifest() ProjectManifest {
	return p.manifest
}

func (p *localProject) Path() string {
	return filepath.Base(p.manifestPath)
}

func (p *localProject) LoadManifest() error {
	content, err := ioutil.ReadFile(p.manifestPath)
	if err != nil {
		return err
	}

	v := validator.New()
	var m ProjectManifest
	err = yaml.UnmarshalWithOptions(
		content,
		&m,
		yaml.Strict(),
		yaml.Validator(v),
	)
	if err != nil {
		return err
	}
	p.manifest = m
	return nil
}

func (p *localProject) SaveManifest() error {
	m, err := yaml.Marshal(p.manifest)
	if err != nil {
		return err
	}

	fs, err := os.Create(p.manifestPath)
	if err != nil {
		return err
	}

	fs.Write(m)
	fs.Close()
	return nil
}

func OpenLocalProject(manifestPath string) (*localProject, error) {
	var err error
	manifestPath, err = filepath.Abs(manifestPath)
	if err != nil {
		return nil, err
	}

	p := &localProject{
		manifestPath: manifestPath,
	}
	if err := p.LoadManifest(); err != nil {
		return nil, err
	} else {
		return p, nil
	}
}

func CreateLocalProject(path string, m ProjectManifest) (*localProject, error) {
	if util.DirExists(path) {
		return nil, fmt.Errorf("dir: %#v already exits", path)
	}
	if err := os.MkdirAll(path, os.ModePerm); err != nil {
		return nil, err
	}

	manifestPath := filepath.Join(path, ManifestFileName)
	p := &localProject{
		manifestPath: manifestPath,
		manifest:     m,
	}
	if err := p.SaveManifest(); err != nil {
		os.RemoveAll(path)
		return nil, err
	} else {
		return p, nil
	}
}
