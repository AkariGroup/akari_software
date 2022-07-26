package daemon

import (
	"github.com/AkariGroup/akari_software/internal/akira/proto"
	"google.golang.org/grpc"
)

func RegisterServicers(s *grpc.Server, d *Daemon) error {
	if system, err := NewSystemServicer(); err != nil {
		return err
	} else {
		proto.RegisterSystemServiceServer(s, system)
	}

	if project, err := NewProjectServicer(d); err != nil {
		return err
	} else {
		proto.RegisterProjectServiceServer(s, project)
	}

	return nil
}
