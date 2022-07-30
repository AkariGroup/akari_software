package daemon

import (
	"context"
	"fmt"
	"log"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"

	"github.com/AkariGroup/akari_software/internal/akira/proto"
	"github.com/AkariGroup/akari_software/internal/akira/service"
)

type AkariServiceServicer struct {
	da *Daemon

	proto.UnimplementedAkariServiceServiceServer
}

func NewAkariServiceServicer(d *Daemon) *AkariServiceServicer {
	return &AkariServiceServicer{
		da: d,
	}
}

func instanceStatusToPb(s service.InstanceStatus) proto.InstanceStatus {
	return proto.InstanceStatus(s)
}

func serviceToPb(c service.ServiceConfig) *proto.Service {
	var ca []string
	for _, v := range c.Capabilities {
		ca = append(ca, string(v))
	}

	return &proto.Service{
		Id:           string(c.Id),
		Name:         c.Name,
		Version:      string(c.Version),
		DisplayName:  c.DisplayName,
		Description:  c.Description,
		Capabilities: ca,
	}
}

func instanceToPb(s service.Instance, c service.ServiceConfig) *proto.ServiceInstance {
	return &proto.ServiceInstance{
		Id:          string(s.Id()),
		Service:     serviceToPb(c),
		DisplayName: s.Config().DisplayName,
		Description: s.Config().Description,
		Status:      instanceStatusToPb(s.Status()),
	}
}

func (m *AkariServiceServicer) ListServices(ctx context.Context, r *emptypb.Empty) (*proto.ListServicesResponse, error) {
	services := m.da.service.Services()
	var ret []*proto.Service
	for _, s := range services {
		ret = append(ret, serviceToPb(s))
	}

	return &proto.ListServicesResponse{
		Services: ret,
	}, nil
}

func (m *AkariServiceServicer) GetService(ctx context.Context, r *proto.GetServiceRequest) (*proto.Service, error) {
	if s, ok := m.da.service.GetService(service.ServiceId(r.Id)); !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("service doesn't exist: %#v", r.Id))
	} else {
		return serviceToPb(s), nil
	}
}

func (m *AkariServiceServicer) ListInstances(ctx context.Context, r *emptypb.Empty) (*proto.ListInstancesResponse, error) {
	services := m.da.service.Instances()
	var ret []*proto.ServiceInstance
	for _, s := range services {
		if c, ok := m.da.service.GetService(s.Config().ServiceId); ok {
			ret = append(ret, instanceToPb(s, c))
		} else {
			log.Printf("failed to find service of id: $#v -> skipped\n", s.Config().ServiceId)
		}
	}

	return &proto.ListInstancesResponse{
		Instances: ret,
	}, nil
}

func (m *AkariServiceServicer) CreateInstance(ctx context.Context, r *proto.CreateInstanceRequest) (*proto.ServiceInstance, error) {
	s, ok := m.da.service.GetService(service.ServiceId(r.ServiceId))
	// NOTE: In order to
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("service doesn't exist: %#v", r.ServiceId))
	}

	// TODO: Use a custom error to change the response type
	// (e.g. Use NotFound eror when the requested service doesn't exist)
	if p, err := m.da.service.CreateInstance(s.Id, r.DisplayName, r.Description); err != nil {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("service doesn't exist: %#v", r.ServiceId))
	} else {
		return instanceToPb(p, s), nil
	}
}

func (m *AkariServiceServicer) GetInstance(ctx context.Context, r *proto.GetInstanceRequest) (*proto.ServiceInstance, error) {
	p, ok := m.da.service.GetInstance(service.InstanceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("instance doesn't exist: %#v", r.Id))
	}
	s, ok := m.da.service.GetService(p.Config().ServiceId)
	if !ok {
		return nil, status.Errorf(codes.Internal, fmt.Sprintf("service removed: %#v", p.Config().ServiceId))
	}
	return instanceToPb(p, s), nil
}

func (m *AkariServiceServicer) RemoveInstance(ctx context.Context, r *proto.RemoveInstanceRequest) (*emptypb.Empty, error) {
	if err := m.da.service.RemoveInstance(service.InstanceId(r.Id)); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("error: %#v", err))
	} else {
		return &emptypb.Empty{}, nil
	}
}

func (m *AkariServiceServicer) StartInstance(ctx context.Context, r *proto.StartInstanceRequest) (*emptypb.Empty, error) {
	s, ok := m.da.service.GetInstance(service.InstanceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("instance doesn't exist: %#v", r.Id))
	}

	if err := s.Start(); err != nil {
		return nil, status.Errorf(codes.Internal, fmt.Sprintf("error: %#v", err))
	} else {
		return &emptypb.Empty{}, nil
	}
}

func (m *AkariServiceServicer) StopInstance(ctx context.Context, r *proto.StopInstanceRequest) (*emptypb.Empty, error) {
	s, ok := m.da.service.GetInstance(service.InstanceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("instance doesn't exist: %#v", r.Id))
	}

	if err := s.Stop(); err != nil {
		return nil, status.Errorf(codes.Internal, fmt.Sprintf("error: %#v", err))
	}

	if r.Terminate {
		if err := s.Terminate(); err != nil {
			return nil, status.Errorf(codes.Internal, fmt.Sprintf("error: %#v", err))
		}
	}
	return &emptypb.Empty{}, nil
}

func (m *AkariServiceServicer) TerminateInstance(ctx context.Context, r *proto.TerminateInstanceRequest) (*emptypb.Empty, error) {
	s, ok := m.da.service.GetInstance(service.InstanceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("instance doesn't exist: %#v", r.Id))
	}

	if err := s.Terminate(); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("error: %#v", err))
	} else {
		return &emptypb.Empty{}, nil
	}
}

func (m *AkariServiceServicer) Open(ctx context.Context, r *proto.OpenRequest) (*proto.OpenResponse, error) {
	s, ok := m.da.service.GetInstance(service.InstanceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("instance doesn't exist: %#v", r.Id))
	}

	if addr, err := s.GetOpenAddress(); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("error: %#v", err))
	} else {
		return &proto.OpenResponse{
			Url: addr,
		}, nil
	}
}

func (m *AkariServiceServicer) OpenProject(ctx context.Context, r *proto.OpenProjectRequest) (*proto.OpenProjectResponse, error) {
	s, ok := m.da.service.GetInstance(service.InstanceId(r.ServiceId))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("instance doesn't exist: %#v", r.ServiceId))
	}

	p, ok := m.da.projects.GetProject(r.ProjectId)
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("project doesn't exist: %#v", r.ProjectId))
	}

	if addr, err := s.GetOpenProjectAddress(p.Path()); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("error: %#v", err))
	} else {
		return &proto.OpenProjectResponse{
			Url: addr,
		}, nil
	}
}
