package daemon

import (
	"context"

	"github.com/AkariGroup/akari_software/internal/akira/proto"
	"google.golang.org/protobuf/types/known/emptypb"
	"google.golang.org/protobuf/types/known/timestamppb"
)

type SystemServicer struct {
	proto.UnimplementedSystemServiceServer
}

func NewSystemServicer() (*SystemServicer, error) {
	return &SystemServicer{}, nil
}

func (s *SystemServicer) GetSystemTime(ctx context.Context, r *emptypb.Empty) (*timestamppb.Timestamp, error) {
	return timestamppb.Now(), nil
}
