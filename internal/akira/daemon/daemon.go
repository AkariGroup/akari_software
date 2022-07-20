package daemon

import (
	"fmt"
	"os"

	"github.com/AkariGroup/akari_software/internal/akira/project"
)

type Daemon struct {
	projects  *project.ProjectManager
	templates *project.TemplateManager
}

const (
	PROJECT_DIR_ENV  = "AKIRA_PROJECT_DIR"
	TEMPLATE_DIR_ENV = "AKIRA_TEMPLATE_DIR"
)

type NewDaemonConfig struct {
	projectDir  *string
	templateDir *string
}

func configOrEnv(v *string, env string) (string, error) {
	if v != nil {
		return *v, nil
	}
	if e, ok := os.LookupEnv(env); ok {
		return e, nil
	} else {
		return "", fmt.Errorf("either config or environ '%s' must be set", env)
	}
}

func NewDaemon(config NewDaemonConfig) (*Daemon, error) {
	projectDir, err := configOrEnv(config.projectDir, PROJECT_DIR_ENV)
	if err != nil {
		return nil, err
	}
	templateDir, err := configOrEnv(config.templateDir, TEMPLATE_DIR_ENV)
	if err != nil {
		return nil, err
	}

	pm := project.NewProjectManager(projectDir)
	pm.UpdateProjects()
	tm := project.NewTemplateManager(templateDir)
	tm.UpdateTemplates()

	return &Daemon{
		projects:  pm,
		templates: tm,
	}, nil
}
