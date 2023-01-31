package service

import (
	"context"
	"sync"

	"github.com/google/uuid"
)

type ServiceId string
type ServiceState int8
type ServiceType int8
type ServiceCapability string

const (
	CapabilityOpen        ServiceCapability = "open"
	CapabilityOpenProject                   = "open_project"
)

const (
	Terminated ServiceState = iota
	Starting
	Running
	Stopping
	Error
	Stopped
)

const (
	ServiceTypeUser ServiceType = iota
	ServiceTypeSystem
)

func NewServiceId() ServiceId {
	return ServiceId(uuid.New().String())
}

type serviceTask struct {
	err error
	wg  sync.WaitGroup
}

func runServiceTask(f func() error) *serviceTask {
	s := &serviceTask{}
	s.wg.Add(1)
	go func() {
		s.err = f()
		s.wg.Done()
	}()

	return s
}

func (s *serviceTask) Wait() error {
	s.wg.Wait()
	return s.err
}

type ServiceTask interface {
	Wait() error
}

type Service interface {
	Id() ServiceId
	Config() ServiceConfig
	Type() ServiceType
	Capabilities() []ServiceCapability

	Start(context.Context) (ServiceTask, error)
	Stop(context.Context) (ServiceTask, error)
	Terminate(context.Context) (ServiceTask, error)
	Clean() error
	State() ServiceState
	Logs() string
	Outputs() (string, string)

	GetOpenAddress(hostName string) (string, error)
	GetOpenProjectAddress(hostName string, projectDir string) (string, error)

	CheckAlive() error
}

type UserService interface {
	Service

	SetConfig(c ServiceConfig) error
	LoadConfig() error
	SaveConfig() error
}
