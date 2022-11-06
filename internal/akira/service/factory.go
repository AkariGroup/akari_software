package service

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/AkariGroup/akari_software/internal/akira/system"
	"github.com/docker/docker/api/types/mount"
)

const (
	AkariRpcServerServiceId        ServiceId = "daa0fee2-2390-43ad-bed8-88d7365311b1"
	AkiraControllerServerServiceId           = "e2ab28cc-5d94-11ed-9b6a-0242ac120002"
)

const (
	AkariRpcServerServicePort                 = 51001
	AkiraControllerServerServicePort          = 52001
	AkariClientConfigHostRpcServer            = "client_configs.d/akari_rpc_service.json"
	AkariClientConfigUseGrpcInBridgeContainer = "client_configs.d/grpc_bridge.json"
	AkariClientConfigEtcPath                  = "/etc/akari/client_config.json"
)

func grpcClientConfigMount(etcDir string) mount.Mount {
	etcPath := filepath.Join(etcDir, AkariClientConfigUseGrpcInBridgeContainer)
	return mount.Mount{
		Type:     mount.TypeBind,
		Source:   etcPath,
		Target:   AkariClientConfigEtcPath,
		ReadOnly: true,
	}
}

func akariRpcServerSystemServiceConfig(etcDir string) (ServiceConfig, system.CreateContainerOption, error) {
	etcPath := filepath.Join(etcDir, AkariClientConfigHostRpcServer)
	if _, err := os.Stat(etcPath); err != nil {
		return ServiceConfig{}, system.CreateContainerOption{}, fmt.Errorf("file error: %#v", err)
	}

	mountsConfig := []mount.Mount{
		{
			Type:     mount.TypeBind,
			Source:   etcPath,
			Target:   AkariClientConfigEtcPath,
			ReadOnly: true,
		},
		{
			Type:   mount.TypeBind,
			Source: "/dev",
			Target: "/dev",
		},
	}
	containerPort := fmt.Sprintf("%d/tcp", AkariRpcServerServicePort)
	serviceConfig := ServiceConfig{
		Id:          AkariRpcServerServiceId,
		ImageId:     NullImageId,
		DisplayName: "AkariRpcServer",
		Description: "gRPC server for host devices",
	}
	containerOpts := system.CreateContainerOption{
		Image: "akarirobot/akari-rpc-server:v1",
		Env:   []string{},
		Ports: map[string]int{
			containerPort: AkariRpcServerServicePort,
		},
		Mounts:      mountsConfig,
		RequireRoot: true,
		Privileged:  true,
	}

	return serviceConfig, containerOpts, nil
}

func akiraControllerServerServiceConfig(etcDir string) (ServiceConfig, system.CreateContainerOption, error) {
	etcPath := filepath.Join(etcDir, AkariClientConfigHostRpcServer)
	if _, err := os.Stat(etcPath); err != nil {
		return ServiceConfig{}, system.CreateContainerOption{}, fmt.Errorf("file error: %#v", err)
	}

	mountsConfig := []mount.Mount{
		grpcClientConfigMount(etcDir),
	}
	containerPort := fmt.Sprintf("%d/tcp", AkiraControllerServerServicePort)
	serviceConfig := ServiceConfig{
		Id:          AkiraControllerServerServiceId,
		ImageId:     NullImageId,
		DisplayName: "ControllerServer",
		Description: "API server for controller page",
	}
	containerOpts := system.CreateContainerOption{
		Image: "akarirobot/akira-controller-server:v1",
		Env:   []string{},
		Ports: map[string]int{
			containerPort: AkiraControllerServerServicePort,
		},
		Mounts:          mountsConfig,
		RequireRoot:     true,
		BindHostGateway: true,
	}

	return serviceConfig, containerOpts, nil
}

func jupyterLabImageConfig() ImageConfig {
	id := ImageId("bca6daa4-b41f-4729-bac3-34f161f9ad91")
	return ImageConfig{
		Id:          id,
		Name:        JupyterLabServiceName,
		Version:     "v1",
		DisplayName: "JupyterLab",
		Description: "Launch a jupyter lab",
		Capabilities: []ServiceCapability{
			CapabilityOpen,
			CapabilityOpenProject,
		},
		ContainerOption: ServiceContainerOption{
			Image: "docker.io/akarirobot/akira-service-jupyter",
		},
	}
}

func vscodeImageConfig() ImageConfig {
	id := ImageId("f7e53430-5123-4be0-a55c-fd545cc56352")
	return ImageConfig{
		Id:          id,
		Name:        VSCodeServiceName,
		Version:     "v1",
		DisplayName: "Visual Studio Code",
		Description: "Launch a Visual Studio Code instance",
		Capabilities: []ServiceCapability{
			CapabilityOpen,
			CapabilityOpenProject,
		},
		ContainerOption: ServiceContainerOption{
			Image: "docker.io/akarirobot/akira-service-vscode",
		},
	}
}
