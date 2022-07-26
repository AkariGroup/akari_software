package main

import (
	"context"
	"fmt"
	"net/http"

	"github.com/AkariGroup/akari_software/internal/akira/proto"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

const (
	DAEMON_GRPC_ENDPOINT = "localhost:30001"
	GATEWAY_PORT         = ":8080"
)

func main() {
	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())}

	if err := proto.RegisterSystemServiceHandlerFromEndpoint(context.Background(), mux, DAEMON_GRPC_ENDPOINT, opts); err != nil {
		panic(err)
	}

	if err := proto.RegisterProjectServiceHandlerFromEndpoint(context.Background(), mux, DAEMON_GRPC_ENDPOINT, opts); err != nil {
		panic(err)
	}

	fmt.Printf("Gateway Started at %s\n", GATEWAY_PORT)
	if err := http.ListenAndServe(GATEWAY_PORT, mux); err != nil {
		panic(err)
	}
}
