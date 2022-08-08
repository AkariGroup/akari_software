package main

import (
	"context"
	"fmt"
	"net/http"

	"github.com/AkariGroup/akari_software/internal/akira/proto"
	"github.com/gorilla/mux"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

const (
	DAEMON_GRPC_ENDPOINT = "localhost:30001"
	GATEWAY_PORT         = ":8080"
)

func createGrpcGateway() (*runtime.ServeMux, error) {
	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())}

	if err := proto.RegisterSystemServiceHandlerFromEndpoint(context.Background(), mux, DAEMON_GRPC_ENDPOINT, opts); err != nil {
		return nil, err
	}

	if err := proto.RegisterProjectServiceHandlerFromEndpoint(context.Background(), mux, DAEMON_GRPC_ENDPOINT, opts); err != nil {
		return nil, err
	}

	if err := proto.RegisterAkariServiceServiceHandlerFromEndpoint(context.Background(), mux, DAEMON_GRPC_ENDPOINT, opts); err != nil {
		return nil, err
	}

	return mux, nil
}

func main() {
	grpcMux, err := createGrpcGateway()
	if err != nil {
		panic(err)
	}

	r := mux.NewRouter()
	r.PathPrefix("/api").Handler(http.StripPrefix("/api", grpcMux))

	fmt.Printf("Gateway Started at %s\n", GATEWAY_PORT)
	if err := http.ListenAndServe(GATEWAY_PORT, r); err != nil {
		panic(err)
	}
}
