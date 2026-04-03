FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY sdk/akari_proto /resources/sdk/akari_proto
COPY sdk/akari_client /resources/sdk/akari_client
RUN uv pip install --system \
        /resources/sdk/akari_client/ \
        /resources/sdk/akari_proto/

COPY internal/akari_rpc_server /resources/sdk/akari_rpc_server
RUN uv pip install --system /resources/sdk/akari_rpc_server/

EXPOSE 51001
CMD ["python3", "-m", "akari_rpc_server.cli"]
