package daemon

import (
	"context"
	"fmt"

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

func instanceStatusToPb(s service.InstanceStatus) proto.ServiceStatus {
	return proto.ServiceStatus(s)
}

func instanceToPb(s service.Instance) *proto.ServiceInstance {
	return &proto.ServiceInstance{
		Id:             string(s.Id()),
		Name:           s.ServiceName(),
		Description:    s.ServiceName(),
		ServiceAddress: s.GetServiceAddress(),
		Status:         instanceStatusToPb(s.Status()),
	}
}

func (m *AkariServiceServicer) ListInstances(ctx context.Context, r *emptypb.Empty) (*proto.ListInstancesResponse, error) {
	services := m.da.service.Instances()
	var ret []*proto.ServiceInstance
	for _, s := range services {
		ret = append(ret, instanceToPb(s))
	}

	return &proto.ListInstancesResponse{
		Instances: ret,
	}, nil
}

func (m *AkariServiceServicer) GetInstance(ctx context.Context, r *proto.GetInstanceRequest) (*proto.ServiceInstance, error) {
	p, ok := m.da.service.GetInstance(service.InstanceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("instance doesn't exist: %#v", r.Id))
	}

	return instanceToPb(p), nil
}

func (m *AkariServiceServicer) TerminateInstance(ctx context.Context, r *proto.TerminateInstanceRequest) (*emptypb.Empty, error) {
	p, ok := m.da.service.GetInstance(service.InstanceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("instance doesn't exist: %#v", r.Id))
	}

	if err := p.Stop(); err != nil {
		return nil, status.Errorf(codes.Internal, fmt.Sprintf("failed to stop service: %#v", err))
	}
	return &emptypb.Empty{}, nil
}

func (m *AkariServiceServicer) LaunchJupyterService(ctx context.Context, r *proto.LaunchJupyterServiceRequest) (*proto.ServiceInstance, error) {
	p, ok := m.da.projects.GetProject(r.ProjectId)
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("project doesn't exist: %#v", r.ProjectId))
	}

	s := service.NewJupyterLabService(
		fmt.Sprintf("JupyterLab for project: %#v", p.Id()),
		p.Path(),
		m.da.docker,
		m.da.service,
	)
	if err := s.Start(); err != nil {
		// TODO: Record logs
		return nil, status.Errorf(codes.Internal, fmt.Sprintf("failed to launch service: %#v", err))
	}

	return instanceToPb(s), nil
}
