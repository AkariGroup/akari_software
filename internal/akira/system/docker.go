package system

import (
	"context"
	"fmt"
	"io"
	"io/ioutil"
	"os/user"
	"strconv"
	"time"

	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/api/types/filters"
	"github.com/docker/docker/api/types/mount"
	"github.com/docker/docker/api/types/network"
	"github.com/docker/docker/client"
	"github.com/docker/docker/pkg/jsonmessage"
	"github.com/docker/docker/pkg/term"
	"github.com/docker/go-connections/nat"
	"github.com/rs/zerolog/log"
)

type ContainerId string

type ContainerType string

const (
	ContainerTypeService ContainerType = "service"
	ContainerTypeDevice                = "device"
)

const (
	AKARI_CONTAINER_MARKER      = "akari"
	AKARI_CONTAINER_TYPE_MARKER = "akari.type"
)

type DockerSystem struct {
	cli          *client.Client
	registryAuth *string
}

func NewDockerSystem(registryAuth *string) (*DockerSystem, error) {
	ctx := context.Background()
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		return nil, err
	}
	cli.NegotiateAPIVersion(ctx)
	return &DockerSystem{
		cli:          cli,
		registryAuth: registryAuth,
	}, nil
}

type CreateContainerOption struct {
	Image             string
	Env               []string
	Ports             map[string]int
	Mounts            []mount.Mount
	RequireRoot       bool
	Privileged        bool
	BindHostGateway   bool
	DeviceCgroupRules []string
}

func (d *DockerSystem) RemoveAllContainers() error {
	filters := filters.NewArgs()
	filters.Add("label", AKARI_CONTAINER_TYPE_MARKER)

	cs, err := d.cli.ContainerList(
		context.Background(),
		types.ContainerListOptions{
			All:     true,
			Filters: filters,
		},
	)
	if err != nil {
		return fmt.Errorf("failed to get containers: %#v", err)
	}

	for _, c := range cs {
		log.Debug().Msgf("Removing container: %s", c.ID)
		d.StopContainer(ContainerId(c.ID), time.Second*10)
		d.RemoveContainer(ContainerId(c.ID))
	}
	return nil
}

func waitPullCompleted(ctx context.Context, in io.ReadCloser, out io.Writer) error {
	fd, isTerminalOut := term.GetFdInfo(out)
	err := jsonmessage.DisplayJSONMessagesStream(in, out, fd, isTerminalOut, nil)
	if err != nil {
		if jerr, ok := err.(*jsonmessage.JSONError); ok {
			if jerr.Code == 0 {
				jerr.Code = 1
			}
			return fmt.Errorf("Status: %s, Code: %d", jerr.Message, jerr.Code)
		}
	}

	return ctx.Err()
}

func (d *DockerSystem) PullImage(image string) error {
	ctx, cancel := context.WithTimeout(context.Background(), time.Minute*10)
	defer cancel()

	opt := types.ImagePullOptions{}
	if d.registryAuth != nil {
		opt.RegistryAuth = *d.registryAuth
	}
	body, err := d.cli.ImagePull(
		context.Background(),
		image,
		opt,
	)
	if err != nil {
		return err
	}
	defer body.Close()
	return waitPullCompleted(ctx, body, ioutil.Discard)
}

func (d *DockerSystem) CreateContainer(config CreateContainerOption) (ContainerId, error) {
	// TODO: Join the container to the gRPC network
	exposedPorts := nat.PortSet{}
	for k := range config.Ports {
		exposedPorts[nat.Port(k)] = struct{}{}
	}

	portBindings := nat.PortMap{}
	for c, h := range config.Ports {
		portBindings[nat.Port(c)] = []nat.PortBinding{{HostPort: strconv.Itoa(h)}}
	}

	var containerUser string
	if !config.RequireRoot {
		if u, err := user.Current(); err != nil {
			return "", fmt.Errorf("failed to get current user: %w", err)
		} else {
			containerUser = fmt.Sprintf("%s:%s", u.Uid, u.Gid)
		}
	}

	containerConfig := container.Config{
		Image:        config.Image,
		Env:          config.Env,
		ExposedPorts: exposedPorts,
		Labels: map[string]string{
			AKARI_CONTAINER_TYPE_MARKER: string(ContainerTypeService),
		},
		User: containerUser,
	}
	var extraHosts []string
	if config.BindHostGateway {
		extraHosts = append(extraHosts, "host.docker.internal:host-gateway")
	}

	hostConfig := container.HostConfig{
		PortBindings: portBindings,
		Mounts:       config.Mounts,
		Privileged:   config.Privileged,
		ExtraHosts:   extraHosts,
		Resources: container.Resources{
			DeviceCgroupRules: config.DeviceCgroupRules,
		},
	}
	container, err := d.cli.ContainerCreate(
		context.Background(),
		&containerConfig,
		&hostConfig,
		&network.NetworkingConfig{},
		nil,
		"",
	)
	if err != nil {
		return "", err
	}

	return ContainerId(container.ID), nil
}

func (d *DockerSystem) StartContainer(id ContainerId) error {
	return d.cli.ContainerStart(
		context.Background(),
		string(id),
		types.ContainerStartOptions{},
	)
}

func (d *DockerSystem) StopContainer(id ContainerId, timeout time.Duration) error {
	if err := d.cli.ContainerStop(context.Background(), string(id), &timeout); err != nil {
		return err
	}

	return nil
}

func (d *DockerSystem) RemoveContainer(id ContainerId) error {
	if err := d.cli.ContainerRemove(
		context.Background(),
		string(id),
		types.ContainerRemoveOptions{
			Force: true,
		},
	); err != nil {
		return err
	}

	return nil
}

func (d *DockerSystem) CheckContainerRunning(id ContainerId) bool {
	inspect, err := d.cli.ContainerInspect(context.Background(), string(id))
	if err != nil {
		return false
	}

	return inspect.State != nil && inspect.State.Running
}
