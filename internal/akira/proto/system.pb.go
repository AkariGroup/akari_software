// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.28.0-devel
// 	protoc        (unknown)
// source: akira_proto/system.proto

package proto

import (
	_ "google.golang.org/genproto/googleapis/api/annotations"
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	emptypb "google.golang.org/protobuf/types/known/emptypb"
	timestamppb "google.golang.org/protobuf/types/known/timestamppb"
	reflect "reflect"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

var File_akira_proto_system_proto protoreflect.FileDescriptor

var file_akira_proto_system_proto_rawDesc = []byte{
	0x0a, 0x18, 0x61, 0x6b, 0x69, 0x72, 0x61, 0x5f, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2f, 0x73, 0x79,
	0x73, 0x74, 0x65, 0x6d, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12, 0x0b, 0x61, 0x6b, 0x69, 0x72,
	0x61, 0x5f, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x1a, 0x1c, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2f,
	0x61, 0x70, 0x69, 0x2f, 0x61, 0x6e, 0x6e, 0x6f, 0x74, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x73, 0x2e,
	0x70, 0x72, 0x6f, 0x74, 0x6f, 0x1a, 0x1b, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2f, 0x70, 0x72,
	0x6f, 0x74, 0x6f, 0x62, 0x75, 0x66, 0x2f, 0x65, 0x6d, 0x70, 0x74, 0x79, 0x2e, 0x70, 0x72, 0x6f,
	0x74, 0x6f, 0x1a, 0x1f, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2f, 0x70, 0x72, 0x6f, 0x74, 0x6f,
	0x62, 0x75, 0x66, 0x2f, 0x74, 0x69, 0x6d, 0x65, 0x73, 0x74, 0x61, 0x6d, 0x70, 0x2e, 0x70, 0x72,
	0x6f, 0x74, 0x6f, 0x32, 0x72, 0x0a, 0x0d, 0x53, 0x79, 0x73, 0x74, 0x65, 0x6d, 0x53, 0x65, 0x72,
	0x76, 0x69, 0x63, 0x65, 0x12, 0x61, 0x0a, 0x0d, 0x47, 0x65, 0x74, 0x53, 0x79, 0x73, 0x74, 0x65,
	0x6d, 0x54, 0x69, 0x6d, 0x65, 0x12, 0x16, 0x2e, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2e, 0x70,
	0x72, 0x6f, 0x74, 0x6f, 0x62, 0x75, 0x66, 0x2e, 0x45, 0x6d, 0x70, 0x74, 0x79, 0x1a, 0x1a, 0x2e,
	0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x62, 0x75, 0x66, 0x2e,
	0x54, 0x69, 0x6d, 0x65, 0x73, 0x74, 0x61, 0x6d, 0x70, 0x22, 0x1c, 0x82, 0xd3, 0xe4, 0x93, 0x02,
	0x16, 0x12, 0x14, 0x2f, 0x73, 0x79, 0x73, 0x74, 0x65, 0x6d, 0x2f, 0x63, 0x75, 0x72, 0x72, 0x65,
	0x6e, 0x74, 0x5f, 0x74, 0x69, 0x6d, 0x65, 0x42, 0x3b, 0x5a, 0x39, 0x67, 0x69, 0x74, 0x68, 0x75,
	0x62, 0x2e, 0x63, 0x6f, 0x6d, 0x2f, 0x41, 0x6b, 0x61, 0x72, 0x69, 0x47, 0x72, 0x6f, 0x75, 0x70,
	0x2f, 0x61, 0x6b, 0x61, 0x72, 0x69, 0x5f, 0x73, 0x6f, 0x66, 0x74, 0x77, 0x61, 0x72, 0x65, 0x2f,
	0x69, 0x6e, 0x74, 0x65, 0x72, 0x6e, 0x61, 0x6c, 0x2f, 0x61, 0x6b, 0x69, 0x72, 0x61, 0x2f, 0x70,
	0x72, 0x6f, 0x74, 0x6f, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var file_akira_proto_system_proto_goTypes = []interface{}{
	(*emptypb.Empty)(nil),         // 0: google.protobuf.Empty
	(*timestamppb.Timestamp)(nil), // 1: google.protobuf.Timestamp
}
var file_akira_proto_system_proto_depIdxs = []int32{
	0, // 0: akira_proto.SystemService.GetSystemTime:input_type -> google.protobuf.Empty
	1, // 1: akira_proto.SystemService.GetSystemTime:output_type -> google.protobuf.Timestamp
	1, // [1:2] is the sub-list for method output_type
	0, // [0:1] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_akira_proto_system_proto_init() }
func file_akira_proto_system_proto_init() {
	if File_akira_proto_system_proto != nil {
		return
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_akira_proto_system_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   0,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_akira_proto_system_proto_goTypes,
		DependencyIndexes: file_akira_proto_system_proto_depIdxs,
	}.Build()
	File_akira_proto_system_proto = out.File
	file_akira_proto_system_proto_rawDesc = nil
	file_akira_proto_system_proto_goTypes = nil
	file_akira_proto_system_proto_depIdxs = nil
}
