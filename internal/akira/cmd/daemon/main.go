package main

import (
	"net"
	"os"

	"github.com/AkariGroup/akari_software/internal/akira/daemon"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"google.golang.org/grpc"
)

const (
	DAEMON_PORT = ":30001"
)

func main() {
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stdout})

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

	log.Info().Msgf("Daemon Started at %s", DAEMON_PORT)
	if err := srv.Serve(lis); err != nil {
		panic(err)
	}
}
