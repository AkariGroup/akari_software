package service

import (
	"errors"
	"fmt"
	"os"
	"strings"

	"github.com/docker/docker/api/types/mount"

	"github.com/AkariGroup/akari_software/internal/akira/internal/util"
	"github.com/AkariGroup/akari_software/internal/akira/system"
)

const (
	JupyterTokenLength            = 20
	JupyterContainerListeningPort = 8080
	JupyterContainerWorkdir       = "/app"
	JupyterContainerVarDir        = "/host_var"
)

type JupyterLab struct {
	*UserServiceProvider
}

type jupyterLabContainerMeta struct {
	servicePort int
	token       string
}

func NewJupyterLab(image ImageConfig, config ServiceConfig, configPath string, opts ServiceManagerOptions) *JupyterLab {
	p := &JupyterLab{}
	p.UserServiceProvider = NewUserServiceProvider(p, config, configPath, image, opts)
	return p
}

func (p *JupyterLab) createContainerConfig() (system.CreateContainerOption, interface{}, error) {
	servicePort, err := util.GetAvailablePort()
	if err != nil {
		return system.CreateContainerOption{}, nil, err
	}

	meta := jupyterLabContainerMeta{
		token:       util.GetRandomByteString(JupyterTokenLength),
		servicePort: servicePort,
	}

	varDir := p.varDir()
	if err := os.MkdirAll(varDir, os.ModePerm); err != nil {
		return system.CreateContainerOption{}, nil, fmt.Errorf("failed to create a var directory: %#v", err)
	}

	mountsConfig := []mount.Mount{
		grpcClientConfigMount(p.opts.EtcDir),
		{
			Type:     mount.TypeBind,
			Source:   p.opts.ProjectRootDir,
			Target:   JupyterContainerWorkdir,
			ReadOnly: false,
		},
		{
			Type:     mount.TypeBind,
			Source:   varDir,
			Target:   JupyterContainerVarDir,
			ReadOnly: false,
		},
	}
	containerPort := fmt.Sprintf("%d/tcp", JupyterContainerListeningPort)
	imageRef := fmt.Sprintf("%s:%s", p.image.ContainerOption.Image, p.image.Version)
	return withOakdAccess(system.CreateContainerOption{
		Image: imageRef,
		Env:   []string{fmt.Sprintf("AKARI_JUPYTER_TOKEN=%s", meta.token), "HOST_UID=1000", "HOST_GID=1000"},
		Ports: map[string]int{
			containerPort: meta.servicePort,
		},
		Mounts:          mountsConfig,
		BindHostGateway: true,
	}), meta, nil
}

func (p *JupyterLab) GetOpenAddress(hostName string) (string, error) {
	_, meta, ok := p.UserServiceProvider.ContainerInfo()

	if ok {
		if meta, ok := meta.(jupyterLabContainerMeta); ok {
			return fmt.Sprintf("http://%s:%d/?token=%s", hostName, meta.servicePort, meta.token), nil
		} else {
			return "", errors.New("invalid internal state")
		}
	} else {
		return "", errors.New("service is not running")
	}
}

func (p *JupyterLab) GetOpenProjectAddress(hostName string, projectDir string) (string, error) {
	if !strings.HasPrefix(projectDir, p.opts.ProjectRootDir) {
		return "", errors.New("project is not in the projects directory")
	}
	relPath := strings.TrimPrefix(projectDir, p.opts.ProjectRootDir)

	_, meta, ok := p.UserServiceProvider.ContainerInfo()

	if ok {
		if meta, ok := meta.(jupyterLabContainerMeta); ok {
			return fmt.Sprintf("http://%s:%d/lab/tree/%s?token=%s", hostName, meta.servicePort, relPath, meta.token), nil
		} else {
			return "", errors.New("invalid internal state")
		}
	} else {
		return "", errors.New("service is not running")
	}
}
