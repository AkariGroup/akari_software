FROM ubuntu:24.04

COPY --from=ghcr.io/astral-sh/uv:0.10.11 /uv /uvx /bin/

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        libxcb1 \
        libgl1 \
        libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY sdk/akari_proto /resources/sdk/akari_proto
COPY sdk/akari_client /resources/sdk/akari_client
RUN uv pip install \
        /resources/sdk/akari_client/ \
        /resources/sdk/akari_proto/

COPY internal/akira_controller_server /resources/sdk/akira_controller_server
RUN uv pip install /resources/sdk/akira_controller_server/
# NOTE: Pre-download models into the docker image in order to minimize starting time of the container
RUN python3 -m akira_controller_server.cli.download_resources

EXPOSE 52001
CMD ["python3", "-m", "akira_controller_server.cli"]
