package service

import (
	"errors"
	"fmt"
	"log"
	"sync"
	"time"

	"github.com/docker/docker/api/types/mount"
	"github.com/google/uuid"

	"github.com/AkariGroup/akari_software/internal/akira/internal/util"
	"github.com/AkariGroup/akari_software/internal/akira/system"
)

const (
	JupyterServiceName            = "JupyterLab"
	JupyterTokenLength            = 20
	JupyterContainerListeningPort = 8080
	JupyterContainerWorkdir       = "/app"
	JupyterImageName              = "akari_jupyter"
)

type JupyterLab struct {
	id          InstanceId
	description string
	docker      *system.DockerSystem
	manager     ServiceManager
	mountDir    string

	token  string
	status InstanceStatus

	servicePort int
	containerId system.ContainerId

	mu sync.Mutex
}

func NewJupyterLabService(description string, mountDir string, d *system.DockerSystem, m ServiceManager) *JupyterLab {
	return &JupyterLab{
		id:          InstanceId(uuid.New().String()),
		description: description,
		docker:      d,
		manager:     m,
		mountDir:    mountDir,

		token:  util.GetRandomByteString(JupyterTokenLength),
		status: Created,
	}
}

func (p *JupyterLab) Id() InstanceId {
	return p.id
}

func (p *JupyterLab) ServiceName() string {
	return JupyterServiceName
}

func (p *JupyterLab) Description() string {
	return p.description
}

func (p *JupyterLab) changeStatus(s InstanceStatus) {
	p.mu.Lock()
	p.status = s
	p.mu.Unlock()
}

func (p *JupyterLab) Start() error {
	if err := p.manager.registerInstance(p); err != nil {
		return err
	}

	err := func() error {
		p.mu.Lock()
		defer p.mu.Unlock()

		if p.status != Created {
			return errors.New("already started")
		}
		p.status = Starting
		return nil
	}()
	if err != nil {
		return err
	}

	p.servicePort, err = util.GetAvailablePort()
	if err != nil {
		p.changeStatus(Error)
		return err
	}

	if err != nil {
		p.changeStatus(Error)
		return err
	}

	mountsConfig := []mount.Mount{
		{
			Type:     mount.TypeBind,
			Source:   p.mountDir,
			Target:   JupyterContainerWorkdir,
			ReadOnly: false,
		},
	}
	containerPort := fmt.Sprintf("%d/tcp", JupyterContainerListeningPort)
	containerId, err := p.docker.CreateContainer(system.CreateContainerOption{
		Image: JupyterImageName,
		Env:   []string{fmt.Sprintf("AKARI_JUPYTER_TOKEN=%s", p.token), "HOST_UID=1000", "HOST_GID=1000"},
		Ports: map[string]int{
			containerPort: p.servicePort,
		},
		Mounts: mountsConfig,
	})
	if err != nil {
		p.changeStatus(Error)
	} else {
		p.containerId = containerId
		p.changeStatus(Running)
	}

	return nil
}

func (p *JupyterLab) GetServiceAddress() string {
	p.mu.Lock()
	defer p.mu.Unlock()

	if p.status == Running {
		return fmt.Sprintf("http://localhost:%d/?token=%s", p.servicePort, p.token)
	} else {
		return ""
	}
}

func (p *JupyterLab) Stop() error {
	err := func() error {
		p.mu.Lock()
		defer p.mu.Unlock()

		if p.status != Running {
			return errors.New("already stopped")
		}
		p.status = Stopping
		return nil
	}()
	if err != nil {
		return err
	}

	timeout := 10 * time.Second
	if err := p.docker.StopContainer(p.containerId, timeout); err != nil {
		p.changeStatus(Error)
		return err
	} else {
		p.changeStatus(Completed)
		return nil
	}
}

func (p *JupyterLab) Remove() {
	p.mu.Lock()
	defer p.mu.Unlock()

	if err := p.docker.RemoveContainer(p.containerId); err != nil {
		log.Printf("got an error while removing the container: %#v", p.containerId)
	}
	defer p.manager.unregisterInstance(p)
}

func (p *JupyterLab) Status() InstanceStatus {
	return p.status
}
