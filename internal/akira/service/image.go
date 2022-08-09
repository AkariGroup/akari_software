package service

type ImageId string
type ImageVersion string

const (
	NullImageId ImageId = ""
)

type ServiceContainerOption struct {
	Image string `json:"image" validate:"required"`
}

type ImageConfig struct {
	// Id is unique to name/version pairs
	Id ImageId `json:"id" validate:"required"`
	// Name is unique through different versions
	Name    string       `json:"name" validate:"required"`
	Version ImageVersion `json:"version" validate:"required"`

	DisplayName     string                 `json:"display_name" validate:"required"`
	Description     string                 `json:"description"`
	Capabilities    []ServiceCapability    `json:"capabilities"`
	ContainerOption ServiceContainerOption `json:"container_option" validate:"required"`
}

const (
	JupyterLabServiceName = "docker.io/akarirobot/akira-service-jupyter"
	VSCodeServiceName     = "docker.io/akarirobot/akira-service-vscode"
)
