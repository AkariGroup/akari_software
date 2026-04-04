FROM ubuntu:24.04

COPY --from=ghcr.io/astral-sh/uv:0.10.11 /uv /uvx /bin/

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        libgl1-mesa-dev \
        libopencv-dev \
        gnome-keyring \
        locales \
        wget \
        python3-dev \
        gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8" \
    TZ="Asia/Tokyo"

RUN curl -fsSL https://code-server.dev/install.sh | sh

RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY sdk/ /resources/sdk/
RUN uv pip install \
        /resources/sdk/akari_client[depthai] \
        /resources/sdk/akari_proto/
COPY internal/akira_services/vscode/entrypoint.sh /entrypoint.sh

RUN mkdir -p /host_var && chmod 777 /host_var
WORKDIR /app
RUN chmod 777 /app

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["code-server", "--bind-addr", "0.0.0.0:8000", "--auth", "none", "--disable-telemetry", "/app"]
