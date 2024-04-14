FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY sdk/akari_proto /resources/sdk/akari_proto
COPY sdk/akari_client /resources/sdk/akari_client
RUN pip install \
        /resources/sdk/akari_client/ \
        /resources/sdk/akari_proto/

COPY internal/akira_controller_server /resources/sdk/akira_controller_server
RUN pip install /resources/sdk/akira_controller_server/
# NOTE: Pre-download models into the docker image in order to minimize starting time of the container
RUN python3 -m akira_controller_server.cli.download_resources

EXPOSE 52001
CMD ["python3", "-m", "akira_controller_server.cli"]
