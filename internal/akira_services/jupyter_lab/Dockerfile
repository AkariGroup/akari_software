FROM python:3.8-buster

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        git \
        wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

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
