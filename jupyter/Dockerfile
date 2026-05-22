FROM quay.io/jupyter/base-notebook:python-3.12

USER root

ENV JUPYTERHUB_CONFIG=/srv/jupyterhub/hub_config.py

RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs npm \
    && npm install -g configurable-http-proxy \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir \
    boto3 \
    joblib \
    jupyterhub==5.2.1 \
    jupyterlab \
    matplotlib \
    pandas \
    psycopg2-binary \
    pyarrow \
    s3fs \
    scikit-learn \
    seaborn \
    sqlalchemy \
    sqlalchemy-trino \
    trino

RUN mkdir -p /srv/jupyterhub-data \
    && chown -R jovyan:users /srv/jupyterhub-data

COPY hub_config.py ${JUPYTERHUB_CONFIG}

USER jovyan
WORKDIR /home/jovyan/work

CMD ["sh", "-c", "jupyterhub -f ${JUPYTERHUB_CONFIG}"]
