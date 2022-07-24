package service

import (
	"fmt"
	"sync"
)

type ServiceManager interface {
	registerInstance(s Instance) error
	unregisterInstance(s Instance)

	Instances() []Instance
	GetInstance(s InstanceId) (Instance, bool)
	TerminateInstance(s InstanceId) error
}

type serviceManager struct {
	instances map[InstanceId]Instance
	mu        sync.RWMutex
}

func NewServiceManager() ServiceManager {
	return &serviceManager{
		instances: make(map[InstanceId]Instance),
	}
}

func (m *serviceManager) registerInstance(s Instance) error {
	m.mu.Lock()
	defer m.mu.Unlock()

	sid := s.Id()
	_, ok := m.instances[sid]
	if ok {
		return fmt.Errorf("instances id conflict: %#v", sid)
	}

	m.instances[s.Id()] = s
	return nil
}

func (m *serviceManager) unregisterInstance(s Instance) {
	m.mu.Lock()
	defer m.mu.Unlock()

	delete(m.instances, s.Id())
}

func (m *serviceManager) Instances() []Instance {
	m.mu.RLock()
	defer m.mu.RUnlock()

	var ret []Instance
	for _, v := range m.instances {
		ret = append(ret, v)
	}
	return ret
}

func (m *serviceManager) GetInstance(id InstanceId) (Instance, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	s, ok := m.instances[id]
	return s, ok
}

func (m *serviceManager) TerminateInstance(id InstanceId) error {
	s, ok := m.GetInstance(id)
	if !ok {
		return fmt.Errorf("instance doesn't exist: %#v", id)
	}

	return s.Stop()
}
