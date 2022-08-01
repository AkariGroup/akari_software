package service

type ServiceId string
type ServiceVersion string
type ServiceCapability string

const (
	CapabilityOpen        ServiceCapability = "open"
	CapabilityOpenProject                   = "open_project"
)

type ServiceContainerOption struct {
	Image string `json:"image" validate:"required"`
}

type ServiceConfig struct {
	// Id is unique to name/version pairs
	Id ServiceId `json:"id" validate:"required"`
	// Name is unique through different versions
	Name    string         `json:"name" validate:"required"`
	Version ServiceVersion `json:"version" validate:"required"`

	DisplayName     string                 `json:"name" validate:"required"`
	Description     string                 `json:"description"`
	Capabilities    []ServiceCapability    `json:"capabilities"`
	ContainerOption ServiceContainerOption `json:"container_option" validate:"required"`
}

const (
	JupyterLabServiceName = "akari-srv.vbcpp.net/jupyer-lab"
)
