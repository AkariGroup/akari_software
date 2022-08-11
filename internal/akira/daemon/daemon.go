package daemon

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/AkariGroup/akari_software/internal/akira/project"
	"github.com/AkariGroup/akari_software/internal/akira/service"
	"github.com/AkariGroup/akari_software/internal/akira/system"
	"github.com/rs/zerolog/log"
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
	ETC_DIR_ENV      = "AKIRA_ETC_DIR"
	VAR_DIR_ENV      = "AKIRA_VAR_DIR"

	DOCKER_REGISTRY_AUTH = "AKIRA_DOCKER_CREDENTIAL"
)

type NewDaemonConfig struct {
	projectDir  *string
	templateDir *string
	etcDir      *string
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

func setupDir(dir string, entry string) (string, error) {
	path := filepath.Join(dir, entry)
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
	etcDir, err := configOrEnv(config.etcDir, ETC_DIR_ENV)
	if err != nil {
		return nil, err
	}
	varDir, err := configOrEnv(config.varDir, VAR_DIR_ENV)
	if err != nil {
		return nil, err
	}

	imageConfigDir, err := setupDir(varDir, "configs/service_images")
	if err != nil {
		return nil, err
	}
	serviceConfigDir, err := setupDir(varDir, "configs/services")
	if err != nil {
		return nil, err
	}
	serviceVarDir, err := setupDir(varDir, "services")
	if err != nil {
		return nil, err
	}

	var dockerAuth *string
	if e, ok := os.LookupEnv(DOCKER_REGISTRY_AUTH); ok {
		dockerAuth = &e
		log.Debug().Msg("use custom credential for docker system")
	}

	docker, err := system.NewDockerSystem(dockerAuth)
	if err != nil {
		return nil, err
	}
	log.Debug().Msg("removing remaining containers of the last session")
	if err := docker.RemoveAllContainers(); err != nil {
		log.Error().Msgf("failed to remove containers: %#v", err)
	}

	pm, err := project.NewProjectManager(projectDir)
	if err != nil {
		return nil, err
	}

	pm.UpdateProjects()
	tm := project.NewTemplateManager(templateDir)
	tm.UpdateTemplates()
	opts := service.ServiceManagerOptions{
		ImageConfigDir:   imageConfigDir,
		ServiceConfigDir: serviceConfigDir,
		ServiceVarDir:    serviceVarDir,
		EtcDir:           etcDir,
		ProjectRootDir:   projectDir,
		Docker:           docker,
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
