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
}

type localProject struct {
	manifest     ProjectManifest
	manifestPath string
	path         string
}

func (p *localProject) Id() ProjectId {
	return p.path
}

func (p *localProject) Name() string {
	return p.manifest.Name
}

func (p *localProject) Manifest() ProjectManifest {
	return p.manifest
}

func (p *localProject) Path() string {
	return p.path
}

func loadManifest(p string) (ProjectManifest, error) {
	content, err := ioutil.ReadFile(p)
	if err != nil {
		return ProjectManifest{}, err
	}

	v := validator.New()
	var m ProjectManifest
	err = yaml.UnmarshalWithOptions(
		content,
		&m,
		yaml.Strict(),
		yaml.Validator(v),
	)
	return m, err
}

func LoadLocalProject(manifestPath string) (*localProject, error) {
	var err error
	manifestPath, err = filepath.Abs(manifestPath)
	if err != nil {
		return nil, err
	}
	manifest, err := loadManifest(manifestPath)
	if err != nil {
		return nil, err
	}

	dirname := filepath.Dir(manifestPath)
	return &localProject{
		manifest:     manifest,
		manifestPath: manifestPath,
		path:         dirname,
	}, nil
}

func CreateEmptyLocalProject(path string, m ProjectManifest) (*localProject, error) {
	manifest, err := yaml.Marshal(m)
	if err != nil {
		return nil, err
	}

	if util.DirExists(path) {
		return nil, fmt.Errorf("dir: %#v already exits", path)
	}
	if err := os.MkdirAll(path, os.ModePerm); err != nil {
		return nil, err
	}

	manifestPath := filepath.Join(path, ManifestFileName)
	fs, err := os.Create(manifestPath)
	if err != nil {
		return nil, err
	}

	fs.Write(manifest)
	fs.Close()

	return LoadLocalProject(manifestPath)
}
