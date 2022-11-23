FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        git \
        locales \
        wget \
        libgl1-mesa-dev \
        libopencv-dev \
        python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8" \
    TZ="Asia/Tokyo"

RUN pip install depthai==2.19.1.0
RUN pip install opencv-python==4.6.0.66
RUN pip install wheel
RUN mkdir -p /wheel \
    && pip wheel -w /wheel jupyterlab==3.4.3
COPY internal/akira_services/jupyter_lab/jupyter_lab_config.py /resources/

COPY sdk/ /resources/sdk/
RUN pip install \
        /resources/sdk/akari_client/ \
        /resources/sdk/akari_proto/
COPY internal/akira_services/jupyter_lab/entrypoint.sh /entrypoint.sh

RUN mkdir -p /host_var && chmod 777 /host_var
WORKDIR /app
RUN chmod 777 /app

EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]
CMD ["jupyter-lab"]
