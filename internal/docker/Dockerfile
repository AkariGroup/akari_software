FROM golang:1.18.2-alpine3.16 AS build

WORKDIR /src
COPY internal/akira .

ARG GOOS linux
ARG GOARCH amd64

ENV GOOS ${GOOS}
ENV GOARCH ${GOARCH}
ENV CGO_ENABLED=0

RUN mkdir -p /build
RUN go build -ldflags="-s -w -extldflags \"-static\"" -o /build/daemon cmd/daemon/main.go
RUN go build -ldflags="-s -w -extldflags \"-static\"" -o /build/gateway cmd/gateway/main.go

# =============================
FROM docker:20.10.17-alpine3.16 as daemon

RUN apk add --no-cache shadow
RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing gosu

WORKDIR /app
COPY internal/docker/daemon-entrypoint.sh /entrypoint.sh
COPY --from=build /build/daemon .
COPY internal/akira_templates /templates

RUN mkdir -p /projects /etc/akira /var/lib/akira

ENV AKIRA_PROJECT_DIR=/projects
ENV AKIRA_TEMPLATE_DIR=/templates
ENV AKIRA_CONFIG_DIR=/etc/akira
ENV AKIRA_VAR_DIR=/var/lib/akira

EXPOSE 30001
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/app/daemon"]

# =============================
FROM scratch as gateway

WORKDIR /app
COPY --from=build /build/gateway .

EXPOSE 8080
CMD ["/app/gateway"]
