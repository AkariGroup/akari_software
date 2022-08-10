package project

import (
	"fmt"
	"os"
	"path"
	"path/filepath"
	"regexp"
	"sync"

	"github.com/AkariGroup/akari_software/internal/akira/internal/util"
	"github.com/rs/zerolog/log"
)

type ProjectManager struct {
	baseDir  string
	projects map[ProjectId]Project

	mu sync.RWMutex
}

func NewProjectManager(baseDir string) (*ProjectManager, error) {
	baseDir, err := filepath.Abs(baseDir)
	if err != nil {
		return nil, err
	}

	if err := os.MkdirAll(baseDir, os.ModePerm); err != nil {
		return nil, err
	}

	return &ProjectManager{
		baseDir:  baseDir,
		projects: make(map[ProjectId]Project),
	}, nil
}

func (m *ProjectManager) registerProject(p Project) error {
	m.projects[p.Id()] = p
	return nil
}

func (m *ProjectManager) clearProjects() {
	for k := range m.projects {
		delete(m.projects, k)
	}
}

func (m *ProjectManager) UpdateProjects() {
	m.mu.Lock()
	defer m.mu.Unlock()

	err := filepath.WalkDir(m.baseDir, func(p string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}

		manifest := path.Join(p, ManifestFileName)
		p = filepath.Join(m.baseDir, p)
		if !util.PathExists(manifest) {
			return nil
		}

		// Detected a file named "akari_manifest.yaml"
		project, err := LoadLocalProject(manifest)
		if err != nil {
			log.Warn().Msgf("error occurred while loading: %s", manifest)
			return nil
		}

		if err := m.registerProject(project); err != nil {
			log.Error().Msgf("error occurred while registering project: %v", project)
			return nil
		}

		return filepath.SkipDir
	})

	if err != nil {
		log.Error().Msgf("error while walking the path: %q", m.baseDir)
		return
	}
}

var isSafeDirName = regexp.MustCompile(`^[A-Za-z0-9_-]+$`)

func (m *ProjectManager) CreateProject(dirname string, manifest ProjectManifest, template Template) (Project, error) {
	if !isSafeDirName.MatchString(dirname) {
		return nil, fmt.Errorf("invalid path: %#v", dirname)
	}

	dir := filepath.Join(m.baseDir, dirname)

	proj, err := func() (Project, error) {
		m.mu.Lock()
		defer m.mu.Unlock()

		if proj, err := CreateEmptyLocalProject(dir, manifest); err != nil {
			return nil, err
		} else {
			m.registerProject(proj)
			return proj, nil
		}
	}()
	if err != nil {
		return nil, err
	}

	if err := template.Setup(dir); err != nil {
		log.Error().Msgf("error occurred while setting up template: %v", err)
	}
	return proj, nil
}

func (m *ProjectManager) ListProjects() map[ProjectId]Project {
	m.mu.RLock()
	defer m.mu.RUnlock()

	projects := make(map[ProjectId]Project)
	for k, p := range m.projects {
		projects[k] = p
	}
	return projects
}

func (m *ProjectManager) GetProject(id ProjectId) (Project, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	p, ok := m.projects[id]
	return p, ok
}
