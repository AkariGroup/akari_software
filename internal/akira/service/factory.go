package service

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/AkariGroup/akari_software/internal/akira/system"
	"github.com/docker/docker/api/types/mount"
)

const (
	AkariRpcServerServicePort                 = 51001
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

func akariRpcServerSystemServiceConfig(etcDir string) (SystemServiceConfig, error) {
	etcPath := filepath.Join(etcDir, AkariClientConfigHostRpcServer)
	if _, err := os.Stat(etcPath); err != nil {
		return SystemServiceConfig{}, fmt.Errorf("file error: %#v", err)
	}

	id := ServiceId("daa0fee2-2390-43ad-bed8-88d7365311b1")
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
	return SystemServiceConfig{
		Id:          id,
		DisplayName: "AkariRpcServer",
		Description: "gRPC server for host devices",
		ContainerOption: system.CreateContainerOption{
			Image: "akarirobot/akari-rpc-server:v1",
			Env:   []string{},
			Ports: map[string]int{
				containerPort: AkariRpcServerServicePort,
			},
			Mounts:      mountsConfig,
			RequireRoot: true,
			Privileged:  true,
		},
	}, nil
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
			Image: "docker.io/akarirobot/akira-jupyter-service",
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
