package project

import (
	"fmt"
	"os"
	"path"
	"path/filepath"
	"sync"

	"github.com/AkariGroup/akari_software/internal/akira/internal/util"
)

type ProjectManager struct {
	baseDir  string
	projects map[ProjectId]Project

	mu sync.RWMutex
}

func NewProjectManager(baseDir string) *ProjectManager {
	return &ProjectManager{
		baseDir:  baseDir,
		projects: make(map[ProjectId]Project),
	}
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
			fmt.Printf("error occured while loading: %s\n", manifest)
			return nil
		}

		if err := m.registerProject(project); err != nil {
			fmt.Printf("error occured while registering project: %v\n", project)
			return nil
		}

		return filepath.SkipDir
	})

	if err != nil {
		fmt.Printf("error while walking the path: %q", m.baseDir)
		return
	}
}

func (m *ProjectManager) CreateProject(name string, manifest ProjectManifest, template Template) (Project, error) {
	dir := filepath.Join(m.baseDir, name)

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
		fmt.Printf("error occured while setting up template: %v\n", err)
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
