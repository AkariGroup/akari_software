FROM python:3.8-slim-buster

COPY sdk/akari_proto /resources/sdk/akari_proto
COPY sdk/akari_client /resources/sdk/akari_client
RUN pip install \
        /resources/sdk/akari_client/ \
        /resources/sdk/akari_proto/

COPY internal/akira_controller_server /resources/sdk/akira_controller_server
# NOTE: In order to avoid resource path issues, install package with editable option
RUN pip install -e /resources/sdk/akira_controller_server/

EXPOSE 52001
CMD ["python3", "-m", "akira_controller_server.cli"]
