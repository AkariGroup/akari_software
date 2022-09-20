FROM python:3.8-buster

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        git \
        gnome-keyring \
        locales \
        wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8" \
    TZ="Asia/Tokyo"

RUN wget -O- https://aka.ms/install-vscode-server/setup.sh | sh

COPY sdk/ /resources/sdk/
RUN pip install \
        /resources/sdk/akari_client/ \
        /resources/sdk/akari_proto/
COPY internal/akira_services/vscode/entrypoint.sh /entrypoint.sh

RUN mkdir -p /host_var && chmod 777 /host_var
WORKDIR /app
RUN chmod 777 /app

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD /bin/bash -c "code-server --accept-server-license-terms serve-local --disable-telemetry --connection-token $AKARI_VSCODE_TOKEN --host 0.0.0.0"
