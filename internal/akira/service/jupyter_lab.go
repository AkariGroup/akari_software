package service

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

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
	config ServiceConfig
	image  ImageConfig
	opts   ServiceManagerOptions
	status ServiceStatus
	token  string

	servicePort int
	containerId *system.ContainerId

	mu sync.Mutex
}

func NewJupyterLab(image ImageConfig, config ServiceConfig, opts ServiceManagerOptions) *JupyterLab {
	return &JupyterLab{
		config: config,
		image:  image,
		opts:   opts,
		status: Terminated,
		token:  util.GetRandomByteString(JupyterTokenLength),
	}
}

func (p *JupyterLab) Id() ServiceId {
	return p.config.Id
}

func (p *JupyterLab) Config() ServiceConfig {
	return p.config
}

func (p *JupyterLab) changeStatus(s ServiceStatus) {
	p.mu.Lock()
	p.status = s
	p.mu.Unlock()
}

func (p *JupyterLab) varDir() string {
	return filepath.Join(p.opts.InstanceVarDir, string(p.config.Id))
}

func (p *JupyterLab) createContainer() (system.ContainerId, error) {
	if p.containerId != nil {
		return *p.containerId, nil
	}

	var err error

	imageRef := fmt.Sprintf("%s:%s", p.image.ContainerOption.Image, p.image.Version)
	err = p.opts.Docker.PullImage(imageRef)
	if err != nil {
		return "", fmt.Errorf("error while pulling image (ref: %#v): %#v)", imageRef, err)
	}

	p.servicePort, err = util.GetAvailablePort()
	if err != nil {
		p.changeStatus(Error)
		return "", err
	}

	varDir := p.varDir()
	if err := os.MkdirAll(varDir, os.ModePerm); err != nil {
		return "", fmt.Errorf("failed to create a var directory: %#v", err)
	}

	mountsConfig := []mount.Mount{
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
	containerId, err := p.opts.Docker.CreateContainer(system.CreateContainerOption{
		Image: imageRef,
		Env:   []string{fmt.Sprintf("AKARI_JUPYTER_TOKEN=%s", p.token), "HOST_UID=1000", "HOST_GID=1000"},
		Ports: map[string]int{
			containerPort: p.servicePort,
		},
		Mounts: mountsConfig,
	})
	return containerId, err
}

func (p *JupyterLab) isRunningState() bool {
	return p.status != Terminated && p.status != Stopped && p.status != Error
}

func (p *JupyterLab) Start() error {
	err := func() error {
		p.mu.Lock()
		defer p.mu.Unlock()

		if p.isRunningState() {
			return errors.New("already started")
		}
		p.status = Starting
		return nil
	}()
	if err != nil {
		return err
	}

	err = func() error {
		cid, err := p.createContainer()
		if err != nil {
			return err
		}

		p.containerId = &cid
		return p.opts.Docker.StartContainer(cid)
	}()
	if err != nil {
		p.changeStatus(Error)
		return err
	}

	p.changeStatus(Running)
	return nil
}

func (p *JupyterLab) getContainerId() (system.ContainerId, bool) {
	if p.containerId == nil {
		return "", false
	} else {
		return *p.containerId, true
	}
}

func (p *JupyterLab) Stop() error {
	cid, err := func() (system.ContainerId, error) {
		p.mu.Lock()
		defer p.mu.Unlock()

		if p.status != Running {
			return "", errors.New("already stopped")
		}
		if cid, ok := p.getContainerId(); !ok {
			return "", errors.New("containerId is null")
		} else {
			p.status = Stopping
			return cid, nil
		}
	}()
	if err != nil {
		return err
	}

	timeout := 10 * time.Second
	if err := p.opts.Docker.StopContainer(cid, timeout); err != nil {
		p.changeStatus(Error)
		return err
	} else {
		p.changeStatus(Stopped)
		return nil
	}
}

func (p *JupyterLab) Terminate() error {
	cid, err := func() (system.ContainerId, error) {
		p.mu.Lock()
		defer p.mu.Unlock()

		if p.status != Terminated && p.status != Stopped {
			return "", errors.New("cannot clean running container")
		}

		cid, ok := p.getContainerId()
		if !ok {
			return "", errors.New("container already removed")
		}
		p.containerId = nil
		return cid, nil
	}()
	if err != nil {
		return err
	}
	p.changeStatus(Terminated)
	if err := p.opts.Docker.RemoveContainer(cid); err != nil {
		return fmt.Errorf("got an error while removing the container: %#v, %#v", p.containerId, err)
	}
	return nil
}

func (p *JupyterLab) Clean() error {
	p.mu.Lock()
	defer p.mu.Unlock()

	if p.status != Terminated {
		return errors.New("cannot remove directory of existing container")
	}

	return os.RemoveAll(p.varDir())
}

func (p *JupyterLab) Status() ServiceStatus {
	return p.status
}

func (p *JupyterLab) GetOpenAddress() (string, error) {
	p.mu.Lock()
	defer p.mu.Unlock()

	if p.status == Running {
		return fmt.Sprintf("http://localhost:%d/?token=%s", p.servicePort, p.token), nil
	} else {
		return "", errors.New("service is not running")
	}
}

func (p *JupyterLab) GetOpenProjectAddress(projectDir string) (string, error) {
	p.mu.Lock()
	defer p.mu.Unlock()

	if !strings.HasPrefix(projectDir, p.opts.ProjectRootDir) {
		return "", errors.New("project is not in the projects directory")
	}

	relPath := strings.TrimPrefix(projectDir, p.opts.ProjectRootDir)
	if p.status == Running {
		return fmt.Sprintf("http://localhost:%d/lab/tree/%s?token=%s", p.servicePort, relPath, p.token), nil
	} else {
		return "", errors.New("service is not running")
	}
}
