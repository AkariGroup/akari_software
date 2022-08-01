package daemon

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/AkariGroup/akari_software/internal/akira/project"
	"github.com/AkariGroup/akari_software/internal/akira/service"
	"github.com/AkariGroup/akari_software/internal/akira/system"
)

type Daemon struct {
	projects  *project.ProjectManager
	templates *project.TemplateManager
	service   service.ServiceManager
	docker    *system.DockerSystem
}

const (
	PROJECT_DIR_ENV  = "AKIRA_PROJECT_DIR"
	TEMPLATE_DIR_ENV = "AKIRA_TEMPLATE_DIR"
	CONFIG_DIR_ENV   = "AKIRA_CONFIG_DIR"
	VAR_DIR_ENV      = "AKIRA_VAR_DIR"

	DOCKER_REGISTRY_AUTH = "AKIRA_DOCKER_CREDENTIAL"
)

type NewDaemonConfig struct {
	projectDir  *string
	templateDir *string
	configDir   *string
	varDir      *string
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

func setupDir(configDir string, entry string) (string, error) {
	path := filepath.Join(configDir, entry)
	if err := os.MkdirAll(path, os.ModePerm); err != nil {
		return "", err
	}
	return path, nil
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
	configDir, err := configOrEnv(config.configDir, CONFIG_DIR_ENV)
	if err != nil {
		return nil, err
	}
	varDir, err := configOrEnv(config.varDir, VAR_DIR_ENV)
	if err != nil {
		return nil, err
	}

	serviceConfigDir, err := setupDir(configDir, "services")
	if err != nil {
		return nil, err
	}
	instanceConfigDir, err := setupDir(configDir, "instances")
	if err != nil {
		return nil, err
	}
	instanceVarDir, err := setupDir(varDir, "instances")

	var dockerAuth *string
	if e, ok := os.LookupEnv(DOCKER_REGISTRY_AUTH); ok {
		dockerAuth = &e
		fmt.Println("use custom credential for docker system")
	}

	docker, err := system.NewDockerSystem(dockerAuth)
	if err != nil {
		return nil, err
	}
	fmt.Println("removing remaining containers of the last session")
	if err := docker.RemoveAllContainers(); err != nil {
		fmt.Printf("failed to remove containers: %#v\n", err)
	}

	pm, err := project.NewProjectManager(projectDir)
	if err != nil {
		return nil, err
	}

	pm.UpdateProjects()
	tm := project.NewTemplateManager(templateDir)
	tm.UpdateTemplates()
	opts := service.ServiceManagerOptions{
		ServiceDir:        serviceConfigDir,
		InstanceConfigDir: instanceConfigDir,
		InstanceVarDir:    instanceVarDir,
		ProjectRootDir:    projectDir,
		Docker:            docker,
	}
	svr, err := service.NewServiceManager(opts)
	if err != nil {
		return nil, err
	}

	return &Daemon{
		projects:  pm,
		templates: tm,
		service:   svr,
		docker:    docker,
	}, nil
}
