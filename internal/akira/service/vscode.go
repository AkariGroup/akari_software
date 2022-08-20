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
	VSCodeTokenLength            = 20
	VSCodeContainerListeningPort = 8000
	VSCodeContainerWorkdir       = "/app"
	VSCodeContainerVarDir        = "/host_var"
)

type VSCode struct {
	*UserServiceProvider
}

type vscodeContainerMeta struct {
	servicePort int
	token       string
}

func NewVSCode(
	image ImageConfig,
	config ServiceConfig,
	configPath string,
	opts ServiceManagerOptions,
) *VSCode {
	p := &VSCode{}
	p.UserServiceProvider = NewUserServiceProvider(p, config, configPath, image, opts)
	return p
}

func (p *VSCode) createContainerConfig() (system.CreateContainerOption, interface{}, error) {
	servicePort, err := util.GetAvailablePort()
	if err != nil {
		return system.CreateContainerOption{}, nil, err
	}

	meta := vscodeContainerMeta{
		token:       util.GetRandomByteString(VSCodeTokenLength),
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
			Target:   VSCodeContainerWorkdir,
			ReadOnly: false,
		},
		{
			Type:     mount.TypeBind,
			Source:   varDir,
			Target:   VSCodeContainerVarDir,
			ReadOnly: false,
		},
	}
	containerPort := fmt.Sprintf("%d/tcp", VSCodeContainerListeningPort)
	imageRef := fmt.Sprintf("%s:%s", p.image.ContainerOption.Image, p.image.Version)
	return system.CreateContainerOption{
		Image: imageRef,
		Env:   []string{fmt.Sprintf("AKARI_VSCODE_TOKEN=%s", meta.token)},
		Ports: map[string]int{
			containerPort: meta.servicePort,
		},
		Mounts:          mountsConfig,
		BindHostGateway: true,
	}, meta, nil
}

func (p *VSCode) GetOpenAddress(hostName string) (string, error) {
	_, meta, ok := p.UserServiceProvider.ContainerInfo()

	if ok {
		if meta, ok := meta.(vscodeContainerMeta); ok {
			return fmt.Sprintf("http://%s:%d/?tkn=%s", hostName, meta.servicePort, meta.token), nil
		} else {
			return "", errors.New("invalid internal state")
		}
	} else {
		return "", errors.New("service is not running")
	}
}

func (p *VSCode) GetOpenProjectAddress(hostName string, projectDir string) (string, error) {
	if !strings.HasPrefix(projectDir, p.opts.ProjectRootDir) {
		return "", errors.New("project is not in the projects directory")
	}
	relPath := strings.TrimPrefix(projectDir, p.opts.ProjectRootDir)

	_, meta, ok := p.UserServiceProvider.ContainerInfo()

	if ok {
		if meta, ok := meta.(vscodeContainerMeta); ok {
			return fmt.Sprintf("http://%s:%d/?tkn=%s&folder=/app/%s", hostName, meta.servicePort, meta.token, relPath), nil
		} else {
			return "", errors.New("invalid internal state")
		}
	} else {
		return "", errors.New("service is not running")
	}
}
