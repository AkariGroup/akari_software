package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"path/filepath"

	"github.com/AkariGroup/akari_software/internal/akira/proto"
	"github.com/gorilla/mux"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

const (
	DEFAULT_DAEMON_ENDPOINT = "localhost:30001"
	GATEWAY_PORT            = ":8080"
)

const (
	STATIC_DIR_ENV      = "AKIRA_GATEWAY_STATIC_DIR"
	DAEMON_ENDPOINT_ENV = "AKIRA_DAEMON_ENDPOINT"
)

func getEnvOrDefault(env string, defaultValue string) string {
	if e, ok := os.LookupEnv(env); ok {
		return e
	} else {
		return defaultValue
	}
}

func createGrpcGateway(daemonEndpoint string) (*runtime.ServeMux, error) {
	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())}

	if err := proto.RegisterSystemServiceHandlerFromEndpoint(context.Background(), mux, daemonEndpoint, opts); err != nil {
		return nil, err
	}

	if err := proto.RegisterProjectServiceHandlerFromEndpoint(context.Background(), mux, daemonEndpoint, opts); err != nil {
		return nil, err
	}

	if err := proto.RegisterAkariServiceServiceHandlerFromEndpoint(context.Background(), mux, daemonEndpoint, opts); err != nil {
		return nil, err
	}

	return mux, nil
}

func createStaticFileServer(staticDir string) http.Handler {
	return http.FileServer(http.Dir(staticDir))
}

func main() {
	staticDir := getEnvOrDefault(STATIC_DIR_ENV, "")
	if staticDir == "" {
		panic(fmt.Errorf("environ: %#v must be set", STATIC_DIR_ENV))
	}

	daemonEndpoint := getEnvOrDefault(DAEMON_ENDPOINT_ENV, DEFAULT_DAEMON_ENDPOINT)
	grpcMux, err := createGrpcGateway(daemonEndpoint)
	if err != nil {
		panic(err)
	}
	static := createStaticFileServer(staticDir)

	r := mux.NewRouter()
	r.PathPrefix("/api").Handler(http.StripPrefix("/api", grpcMux))
	r.PathPrefix("/static").Handler(static)
	r.PathPrefix("/images").Handler(static)
	r.PathPrefix("/").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, filepath.Join(staticDir, "index.html"))
	})

	fmt.Printf("Gateway Started at %s\n", GATEWAY_PORT)
	if err := http.ListenAndServe(GATEWAY_PORT, r); err != nil {
		panic(err)
	}
}
