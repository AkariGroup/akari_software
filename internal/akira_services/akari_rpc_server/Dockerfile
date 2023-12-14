FROM python:3.11-slim-buster

COPY sdk/akari_proto /resources/sdk/akari_proto
COPY sdk/akari_client /resources/sdk/akari_client
RUN pip install \
        /resources/sdk/akari_client/ \
        /resources/sdk/akari_proto/

COPY internal/akari_rpc_server /resources/sdk/akari_rpc_server
RUN pip install /resources/sdk/akari_rpc_server/

EXPOSE 51001
CMD ["python3", "-m", "akari_rpc_server.cli"]
