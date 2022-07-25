package system

import (
	"context"
	"fmt"
	"os/user"
	"strconv"
	"time"

	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/api/types/mount"
	"github.com/docker/docker/api/types/network"
	"github.com/docker/docker/client"
	"github.com/docker/go-connections/nat"
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
	cli        *client.Client
	containers map[ContainerId]struct{}
}

func NewDockerSystem() (*DockerSystem, error) {
	ctx := context.Background()
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		return nil, err
	}
	cli.NegotiateAPIVersion(ctx)
	return &DockerSystem{
		cli:        cli,
		containers: map[ContainerId]struct{}{},
	}, nil
}

type CreateContainerOption struct {
	Image  string
	Env    []string
	Ports  map[string]int
	Mounts []mount.Mount
	RequireRoot bool
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
	hostConfig := container.HostConfig{
		PortBindings: portBindings,
		Mounts:       config.Mounts,
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

	if err := d.cli.ContainerStart(
		context.Background(),
		container.ID,
		types.ContainerStartOptions{},
	); err != nil {
		d.cli.ContainerRemove(
			context.Background(),
			container.ID,
			types.ContainerRemoveOptions{},
		)
		return "", err
	}

	id := ContainerId(container.ID)
	d.containers[id] = struct{}{}
	return id, nil
}

func (d *DockerSystem) StopContainer(id ContainerId, timeout time.Duration) error {
	if err := d.cli.ContainerStop(context.Background(), string(id), &timeout); err != nil {
		return err
	}

	return nil
}

func (d *DockerSystem) RemoveContainer(id ContainerId) error {
	if err := d.cli.ContainerRemove(context.Background(), string(id), types.ContainerRemoveOptions{}); err != nil {
		return err
	}
	delete(d.containers, id)

	return nil
}
