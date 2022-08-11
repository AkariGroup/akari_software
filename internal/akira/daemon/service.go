package daemon

import (
	"context"
	"fmt"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"

	"github.com/AkariGroup/akari_software/internal/akira/proto"
	"github.com/AkariGroup/akari_software/internal/akira/service"
	"github.com/rs/zerolog/log"
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

func capabilitiesToPb(caps []service.ServiceCapability) []string {
	var ret []string
	for _, v := range caps {
		ret = append(ret, string(v))
	}
	return ret
}

func serviceStatusToPb(s service.ServiceStatus) proto.ServiceStatus {
	return proto.ServiceStatus(s)
}

func serviceTypeToPb(s service.ServiceType) proto.ServiceType {
	return proto.ServiceType(s)
}

func imageToPb(c service.ImageConfig) *proto.ServiceImage {
	return &proto.ServiceImage{
		Id:           string(c.Id),
		Name:         c.Name,
		Version:      string(c.Version),
		DisplayName:  c.DisplayName,
		Description:  c.Description,
		Capabilities: capabilitiesToPb(c.Capabilities),
	}
}

func serviceToPb(m service.ServiceManager, s service.Service) *proto.Service {
	var image *proto.ServiceImage = nil
	if imgId := s.ImageId(); imgId != service.NullImageId {
		if c, ok := m.GetImage(imgId); ok {
			image = imageToPb(c)
		} else {
			log.Error().Msgf("failed to find service of id: %#v", imgId)
		}
	}

	return &proto.Service{
		Id:           string(s.Id()),
		Image:        image,
		DisplayName:  s.DisplayName(),
		Description:  s.Description(),
		Status:       serviceStatusToPb(s.Status()),
		Type:         serviceTypeToPb(s.Type()),
		Capabilities: capabilitiesToPb(s.Capabilities()),
	}
}

func (m *AkariServiceServicer) ListImages(ctx context.Context, r *emptypb.Empty) (*proto.ListImagesResponse, error) {
	services := m.da.service.Images()
	var ret []*proto.ServiceImage
	for _, s := range services {
		ret = append(ret, imageToPb(s))
	}

	return &proto.ListImagesResponse{
		Images: ret,
	}, nil
}

func (m *AkariServiceServicer) GetImage(ctx context.Context, r *proto.GetImageRequest) (*proto.ServiceImage, error) {
	if s, ok := m.da.service.GetImage(service.ImageId(r.Id)); !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("service doesn't exist: %#v", r.Id))
	} else {
		return imageToPb(s), nil
	}
}

func (m *AkariServiceServicer) ListServices(ctx context.Context, r *emptypb.Empty) (*proto.ListServicesResponse, error) {
	services := m.da.service.Services()
	var ret []*proto.Service
	for _, s := range services {
		ret = append(ret, serviceToPb(m.da.service, s))
	}

	return &proto.ListServicesResponse{
		Services: ret,
	}, nil
}

func (m *AkariServiceServicer) CreateService(ctx context.Context, r *proto.CreateServiceRequest) (*proto.Service, error) {
	s, ok := m.da.service.GetImage(service.ImageId(r.ImageId))
	// NOTE: In order to
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("service doesn't exist: %#v", r.ImageId))
	}

	// TODO: Use a custom error to change the response type
	// (e.g. Use NotFound eror when the requested service doesn't exist)
	if p, err := m.da.service.CreateUserService(s.Id, r.DisplayName, r.Description); err != nil {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("failed to create service: %#v", err))
	} else {
		return serviceToPb(m.da.service, p), nil
	}
}

func (m *AkariServiceServicer) GetService(ctx context.Context, r *proto.GetServiceRequest) (*proto.Service, error) {
	p, ok := m.da.service.GetService(service.ServiceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("service doesn't exist: %#v", r.Id))
	}
	return serviceToPb(m.da.service, p), nil
}

func (m *AkariServiceServicer) RemoveService(ctx context.Context, r *proto.RemoveServiceRequest) (*emptypb.Empty, error) {
	if err := m.da.service.RemoveUserService(service.ServiceId(r.Id)); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("error: %#v", err))
	} else {
		return &emptypb.Empty{}, nil
	}
}

func (m *AkariServiceServicer) StartService(ctx context.Context, r *proto.StartServiceRequest) (*emptypb.Empty, error) {
	s, ok := m.da.service.GetService(service.ServiceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("service doesn't exist: %#v", r.Id))
	}

	if err := s.Start(); err != nil {
		return nil, status.Errorf(codes.Internal, fmt.Sprintf("error: %#v", err))
	} else {
		return &emptypb.Empty{}, nil
	}
}

func (m *AkariServiceServicer) StopService(ctx context.Context, r *proto.StopServiceRequest) (*emptypb.Empty, error) {
	s, ok := m.da.service.GetService(service.ServiceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("service doesn't exist: %#v", r.Id))
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

func (m *AkariServiceServicer) TerminateService(ctx context.Context, r *proto.TerminateServiceRequest) (*emptypb.Empty, error) {
	s, ok := m.da.service.GetService(service.ServiceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("service doesn't exist: %#v", r.Id))
	}

	if err := s.Terminate(); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("error: %#v", err))
	} else {
		return &emptypb.Empty{}, nil
	}
}

func (m *AkariServiceServicer) Open(ctx context.Context, r *proto.OpenRequest) (*proto.OpenResponse, error) {
	s, ok := m.da.service.GetService(service.ServiceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("service doesn't exist: %#v", r.Id))
	}

	if addr, err := s.GetOpenAddress(r.ApiHostname); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("error: %#v", err))
	} else {
		return &proto.OpenResponse{
			Url: addr,
		}, nil
	}
}

func (m *AkariServiceServicer) OpenProject(ctx context.Context, r *proto.OpenProjectRequest) (*proto.OpenProjectResponse, error) {
	s, ok := m.da.service.GetService(service.ServiceId(r.Id))
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("service doesn't exist: %#v", r.Id))
	}

	p, ok := m.da.projects.GetProject(r.ProjectId)
	if !ok {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("project doesn't exist: %#v", r.ProjectId))
	}

	if addr, err := s.GetOpenProjectAddress(r.ApiHostname, p.Path()); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("error: %#v", err))
	} else {
		return &proto.OpenProjectResponse{
			Url: addr,
		}, nil
	}
}
