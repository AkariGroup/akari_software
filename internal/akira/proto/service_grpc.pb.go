// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             (unknown)
// source: akira_proto/service.proto

package proto

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	emptypb "google.golang.org/protobuf/types/known/emptypb"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// AkariServiceServiceClient is the client API for AkariServiceService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type AkariServiceServiceClient interface {
	ListImages(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*ListImagesResponse, error)
	GetImage(ctx context.Context, in *GetImageRequest, opts ...grpc.CallOption) (*ServiceImage, error)
	ListServices(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*ListServicesResponse, error)
	CreateService(ctx context.Context, in *CreateServiceRequest, opts ...grpc.CallOption) (*Service, error)
	GetService(ctx context.Context, in *GetServiceRequest, opts ...grpc.CallOption) (*Service, error)
	RemoveService(ctx context.Context, in *RemoveServiceRequest, opts ...grpc.CallOption) (*emptypb.Empty, error)
	StartService(ctx context.Context, in *StartServiceRequest, opts ...grpc.CallOption) (*emptypb.Empty, error)
	StopService(ctx context.Context, in *StopServiceRequest, opts ...grpc.CallOption) (*emptypb.Empty, error)
	TerminateService(ctx context.Context, in *TerminateServiceRequest, opts ...grpc.CallOption) (*emptypb.Empty, error)
	Open(ctx context.Context, in *OpenRequest, opts ...grpc.CallOption) (*OpenResponse, error)
	OpenProject(ctx context.Context, in *OpenProjectRequest, opts ...grpc.CallOption) (*OpenProjectResponse, error)
}

type akariServiceServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewAkariServiceServiceClient(cc grpc.ClientConnInterface) AkariServiceServiceClient {
	return &akariServiceServiceClient{cc}
}

func (c *akariServiceServiceClient) ListImages(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*ListImagesResponse, error) {
	out := new(ListImagesResponse)
	err := c.cc.Invoke(ctx, "/akira_proto.AkariServiceService/ListImages", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *akariServiceServiceClient) GetImage(ctx context.Context, in *GetImageRequest, opts ...grpc.CallOption) (*ServiceImage, error) {
	out := new(ServiceImage)
	err := c.cc.Invoke(ctx, "/akira_proto.AkariServiceService/GetImage", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *akariServiceServiceClient) ListServices(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*ListServicesResponse, error) {
	out := new(ListServicesResponse)
	err := c.cc.Invoke(ctx, "/akira_proto.AkariServiceService/ListServices", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *akariServiceServiceClient) CreateService(ctx context.Context, in *CreateServiceRequest, opts ...grpc.CallOption) (*Service, error) {
	out := new(Service)
	err := c.cc.Invoke(ctx, "/akira_proto.AkariServiceService/CreateService", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *akariServiceServiceClient) GetService(ctx context.Context, in *GetServiceRequest, opts ...grpc.CallOption) (*Service, error) {
	out := new(Service)
	err := c.cc.Invoke(ctx, "/akira_proto.AkariServiceService/GetService", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *akariServiceServiceClient) RemoveService(ctx context.Context, in *RemoveServiceRequest, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, "/akira_proto.AkariServiceService/RemoveService", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *akariServiceServiceClient) StartService(ctx context.Context, in *StartServiceRequest, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, "/akira_proto.AkariServiceService/StartService", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *akariServiceServiceClient) StopService(ctx context.Context, in *StopServiceRequest, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, "/akira_proto.AkariServiceService/StopService", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *akariServiceServiceClient) TerminateService(ctx context.Context, in *TerminateServiceRequest, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, "/akira_proto.AkariServiceService/TerminateService", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *akariServiceServiceClient) Open(ctx context.Context, in *OpenRequest, opts ...grpc.CallOption) (*OpenResponse, error) {
	out := new(OpenResponse)
	err := c.cc.Invoke(ctx, "/akira_proto.AkariServiceService/Open", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *akariServiceServiceClient) OpenProject(ctx context.Context, in *OpenProjectRequest, opts ...grpc.CallOption) (*OpenProjectResponse, error) {
	out := new(OpenProjectResponse)
	err := c.cc.Invoke(ctx, "/akira_proto.AkariServiceService/OpenProject", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// AkariServiceServiceServer is the server API for AkariServiceService service.
// All implementations must embed UnimplementedAkariServiceServiceServer
// for forward compatibility
type AkariServiceServiceServer interface {
	ListImages(context.Context, *emptypb.Empty) (*ListImagesResponse, error)
	GetImage(context.Context, *GetImageRequest) (*ServiceImage, error)
	ListServices(context.Context, *emptypb.Empty) (*ListServicesResponse, error)
	CreateService(context.Context, *CreateServiceRequest) (*Service, error)
	GetService(context.Context, *GetServiceRequest) (*Service, error)
	RemoveService(context.Context, *RemoveServiceRequest) (*emptypb.Empty, error)
	StartService(context.Context, *StartServiceRequest) (*emptypb.Empty, error)
	StopService(context.Context, *StopServiceRequest) (*emptypb.Empty, error)
	TerminateService(context.Context, *TerminateServiceRequest) (*emptypb.Empty, error)
	Open(context.Context, *OpenRequest) (*OpenResponse, error)
	OpenProject(context.Context, *OpenProjectRequest) (*OpenProjectResponse, error)
	mustEmbedUnimplementedAkariServiceServiceServer()
}

// UnimplementedAkariServiceServiceServer must be embedded to have forward compatible implementations.
type UnimplementedAkariServiceServiceServer struct {
}

func (UnimplementedAkariServiceServiceServer) ListImages(context.Context, *emptypb.Empty) (*ListImagesResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method ListImages not implemented")
}
func (UnimplementedAkariServiceServiceServer) GetImage(context.Context, *GetImageRequest) (*ServiceImage, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetImage not implemented")
}
func (UnimplementedAkariServiceServiceServer) ListServices(context.Context, *emptypb.Empty) (*ListServicesResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method ListServices not implemented")
}
func (UnimplementedAkariServiceServiceServer) CreateService(context.Context, *CreateServiceRequest) (*Service, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CreateService not implemented")
}
func (UnimplementedAkariServiceServiceServer) GetService(context.Context, *GetServiceRequest) (*Service, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetService not implemented")
}
func (UnimplementedAkariServiceServiceServer) RemoveService(context.Context, *RemoveServiceRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method RemoveService not implemented")
}
func (UnimplementedAkariServiceServiceServer) StartService(context.Context, *StartServiceRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method StartService not implemented")
}
func (UnimplementedAkariServiceServiceServer) StopService(context.Context, *StopServiceRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method StopService not implemented")
}
func (UnimplementedAkariServiceServiceServer) TerminateService(context.Context, *TerminateServiceRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method TerminateService not implemented")
}
func (UnimplementedAkariServiceServiceServer) Open(context.Context, *OpenRequest) (*OpenResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Open not implemented")
}
func (UnimplementedAkariServiceServiceServer) OpenProject(context.Context, *OpenProjectRequest) (*OpenProjectResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method OpenProject not implemented")
}
func (UnimplementedAkariServiceServiceServer) mustEmbedUnimplementedAkariServiceServiceServer() {}

// UnsafeAkariServiceServiceServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to AkariServiceServiceServer will
// result in compilation errors.
type UnsafeAkariServiceServiceServer interface {
	mustEmbedUnimplementedAkariServiceServiceServer()
}

func RegisterAkariServiceServiceServer(s grpc.ServiceRegistrar, srv AkariServiceServiceServer) {
	s.RegisterService(&AkariServiceService_ServiceDesc, srv)
}

func _AkariServiceService_ListImages_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(emptypb.Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AkariServiceServiceServer).ListImages(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/akira_proto.AkariServiceService/ListImages",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AkariServiceServiceServer).ListImages(ctx, req.(*emptypb.Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _AkariServiceService_GetImage_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetImageRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AkariServiceServiceServer).GetImage(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/akira_proto.AkariServiceService/GetImage",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AkariServiceServiceServer).GetImage(ctx, req.(*GetImageRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _AkariServiceService_ListServices_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(emptypb.Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AkariServiceServiceServer).ListServices(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/akira_proto.AkariServiceService/ListServices",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AkariServiceServiceServer).ListServices(ctx, req.(*emptypb.Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _AkariServiceService_CreateService_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(CreateServiceRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AkariServiceServiceServer).CreateService(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/akira_proto.AkariServiceService/CreateService",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AkariServiceServiceServer).CreateService(ctx, req.(*CreateServiceRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _AkariServiceService_GetService_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetServiceRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AkariServiceServiceServer).GetService(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/akira_proto.AkariServiceService/GetService",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AkariServiceServiceServer).GetService(ctx, req.(*GetServiceRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _AkariServiceService_RemoveService_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(RemoveServiceRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AkariServiceServiceServer).RemoveService(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/akira_proto.AkariServiceService/RemoveService",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AkariServiceServiceServer).RemoveService(ctx, req.(*RemoveServiceRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _AkariServiceService_StartService_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(StartServiceRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AkariServiceServiceServer).StartService(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/akira_proto.AkariServiceService/StartService",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AkariServiceServiceServer).StartService(ctx, req.(*StartServiceRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _AkariServiceService_StopService_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(StopServiceRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AkariServiceServiceServer).StopService(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/akira_proto.AkariServiceService/StopService",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AkariServiceServiceServer).StopService(ctx, req.(*StopServiceRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _AkariServiceService_TerminateService_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(TerminateServiceRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AkariServiceServiceServer).TerminateService(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/akira_proto.AkariServiceService/TerminateService",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AkariServiceServiceServer).TerminateService(ctx, req.(*TerminateServiceRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _AkariServiceService_Open_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(OpenRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AkariServiceServiceServer).Open(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/akira_proto.AkariServiceService/Open",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AkariServiceServiceServer).Open(ctx, req.(*OpenRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _AkariServiceService_OpenProject_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(OpenProjectRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AkariServiceServiceServer).OpenProject(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/akira_proto.AkariServiceService/OpenProject",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AkariServiceServiceServer).OpenProject(ctx, req.(*OpenProjectRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// AkariServiceService_ServiceDesc is the grpc.ServiceDesc for AkariServiceService service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var AkariServiceService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "akira_proto.AkariServiceService",
	HandlerType: (*AkariServiceServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "ListImages",
			Handler:    _AkariServiceService_ListImages_Handler,
		},
		{
			MethodName: "GetImage",
			Handler:    _AkariServiceService_GetImage_Handler,
		},
		{
			MethodName: "ListServices",
			Handler:    _AkariServiceService_ListServices_Handler,
		},
		{
			MethodName: "CreateService",
			Handler:    _AkariServiceService_CreateService_Handler,
		},
		{
			MethodName: "GetService",
			Handler:    _AkariServiceService_GetService_Handler,
		},
		{
			MethodName: "RemoveService",
			Handler:    _AkariServiceService_RemoveService_Handler,
		},
		{
			MethodName: "StartService",
			Handler:    _AkariServiceService_StartService_Handler,
		},
		{
			MethodName: "StopService",
			Handler:    _AkariServiceService_StopService_Handler,
		},
		{
			MethodName: "TerminateService",
			Handler:    _AkariServiceService_TerminateService_Handler,
		},
		{
			MethodName: "Open",
			Handler:    _AkariServiceService_Open_Handler,
		},
		{
			MethodName: "OpenProject",
			Handler:    _AkariServiceService_OpenProject_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "akira_proto/service.proto",
}