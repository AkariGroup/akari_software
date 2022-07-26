package service

type InstanceId string
type InstanceStatus int8

const (
	Created InstanceStatus = iota
	Starting
	Running
	Stopping
	Error
	Completed
)

type Instance interface {
	Id() InstanceId
	ServiceName() string
	Description() string

	Start() error
	Stop() error
	Remove()
	Status() InstanceStatus
	GetServiceAddress() string
}
