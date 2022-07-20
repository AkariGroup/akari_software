package main

import (
	"fmt"
	"net"

	"github.com/AkariGroup/akari_software/internal/akira/daemon"
	"google.golang.org/grpc"
)

const (
	DAEMON_PORT = ":30001"
)

func main() {
	srv := grpc.NewServer()
	d, err := daemon.NewDaemon(daemon.NewDaemonConfig{})
	if err != nil {
		panic(err)
	}

	if err := daemon.RegisterServicers(srv, d); err != nil {
		panic(err)
	}

	lis, err := net.Listen("tcp", DAEMON_PORT)
	if err != nil {
		panic(err)
	}

	fmt.Printf("Daemon Started at %s\n", DAEMON_PORT)
	if err := srv.Serve(lis); err != nil {
		panic(err)
	}
}
