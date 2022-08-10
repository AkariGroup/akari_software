package project

import (
	"io/ioutil"
	"path/filepath"
	"strings"
	"sync"

	"github.com/go-playground/validator/v10"
	yaml "github.com/goccy/go-yaml"
	cp "github.com/otiai10/copy"
	"github.com/rs/zerolog/log"
)

const (
	METADATA_FILENAME = "akari_template.yaml"
)

type TemplateId = string

type TemplateMetadata struct {
	Name        string   `json:"name" validate:"required"`
	Version     string   `json:"version" validate:"required"`
	Description string   `json:"description"`
	Author      string   `json:"author"`
	Url         string   `json:"url"`
	Tags        []string `json:"tags"`
}

type Template interface {
	Id() TemplateId
	Metadata() TemplateMetadata
	Setup(dir string) error
}

type localTemplate struct {
	id   TemplateId
	meta TemplateMetadata
	dir  string
}

func (t *localTemplate) Id() string {
	return t.id
}

func (t *localTemplate) Metadata() TemplateMetadata {
	return t.meta
}

func (t *localTemplate) Setup(d string) error {
	metaPath := filepath.Join(t.dir, METADATA_FILENAME)
	opts := cp.Options{
		Skip: func(src string) (bool, error) {
			return src == metaPath, nil
		},
	}
	return cp.Copy(t.dir, d, opts)
}

type TemplateManager struct {
	baseDir   string
	templates map[TemplateId]Template

	mu sync.RWMutex
}

func NewTemplateManager(baseDir string) *TemplateManager {
	return &TemplateManager{
		baseDir:   baseDir,
		templates: make(map[TemplateId]Template),
	}
}

func (m *TemplateManager) ListTemplates() map[TemplateId]Template {
	m.mu.RLock()
	defer m.mu.RUnlock()

	templates := make(map[TemplateId]Template)
	for k, p := range m.templates {
		templates[k] = p
	}
	return templates
}

func (m *TemplateManager) LookupTemplate(id TemplateId) (Template, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	t, ok := m.templates[id]
	return t, ok
}

func (m *TemplateManager) clearTemplates() {
	for k := range m.templates {
		delete(m.templates, k)
	}
}

func loadMetadata(p string) (TemplateMetadata, error) {
	content, err := ioutil.ReadFile(p)
	if err != nil {
		return TemplateMetadata{}, err
	}

	v := validator.New()
	var meta TemplateMetadata
	err = yaml.UnmarshalWithOptions(
		content,
		&meta,
		yaml.Strict(),
		yaml.Validator(v),
	)
	return meta, err
}

func (m *TemplateManager) UpdateTemplates() {
	m.mu.Lock()
	defer m.mu.Unlock()

	m.clearTemplates()

	files, err := ioutil.ReadDir(m.baseDir)
	if err != nil {
		log.Error().Msgf("error while scanning templates: %#v", err)
		return
	}

	for _, f := range files {
		if !f.IsDir() {
			continue
		}
		p := filepath.Join(m.baseDir, f.Name())
		base := filepath.Base(p)
		if strings.HasPrefix(base, ".") {
			continue
		}

		if meta, err := loadMetadata(filepath.Join(p, METADATA_FILENAME)); err != nil {
			log.Warn().Msgf("error while loading metadata: %#v", err)
		} else {
			m.templates[base] = &localTemplate{
				id:   base,
				meta: meta,
				dir:  p,
			}
		}
	}
}
