FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        git \
        libgl1-mesa-dev \
        libopencv-dev \
        locales \
        wget \
        python3-pip \
        python3-venv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8" \
    TZ="Asia/Tokyo"

RUN pip install wheel
RUN mkdir -p /wheel \
    && pip wheel -w /wheel jupyterlab==3.4.3
COPY internal/akira_services/jupyter_lab/jupyter_lab_config.py /resources/

COPY sdk/ /resources/sdk/
RUN pip install \
        /resources/sdk/akari_client[depthai] \
        /resources/sdk/akari_proto/
COPY internal/akira_services/jupyter_lab/entrypoint.sh /entrypoint.sh
ENV JUPYTER_PREFER_ENV_PATH=1

RUN mkdir -p /host_var && chmod 777 /host_var
WORKDIR /app
RUN chmod 777 /app

EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]
CMD ["jupyter-lab"]
