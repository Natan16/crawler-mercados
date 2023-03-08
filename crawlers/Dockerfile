FROM python:3.10

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        gdal-bin \
        wait-for-it \
        curl \
        gpg && \
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc \
      | gpg --dearmor \
      | tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main" > /etc/apt/sources.list.d/postgresql.list && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        jq \
        libgdal-dev \
        locales \
        supervisor \
        libmagic-dev \
        build-essential \
        # Shapely dep
        libgeos-dev \
        # usado durante o CI para verificar se mudou coisa sem ser no frontend
        git \
        # cffi dep
        libffi-dev \
        # lxml dep
        libxml2-dev libxslt1-dev \
        # cryptography dep
        rustc cargo \
        # pg_dump/pg_restore no CI
        postgresql-client-14 \
        npm  && \
    mkdir -p /run/nginx && \
    pip install uwsgi uwsgitop poetry

# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh && \
    echo "export LS_OPTIONS='--color=auto'" >>~/.bashrc && \
    echo "alias ls='ls \$LS_OPTIONS'" >>~/.bashrc && \
    echo "alias ll='ls \$LS_OPTIONS -l'" >>~/.bashrc && \
    echo "alias l='ls \$LS_OPTIONS -lA'" >>~/.bashrc

RUN mkdir /dkdata
WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
  && poetry install

COPY frontend/package.json frontend/package.json
COPY frontend/package-lock.json frontend/package-lock.json
RUN cd frontend && npm install && npm install -g pm2
COPY frontend frontend
RUN cd frontend && npm run build

ENV SHELL=/bin/bash PYTHONUNBUFFERED=1 NODE_ENV=production API_MOCK=0 PYTHONIOENCODING=UTF-8 LANG=en_US.UTF-8 DJANGO_STATIC_ROOT=/dkdata/static DJANGO_LOG_FILE=/dkdata/crawlers.log UWSGI_PROCESSES=3 PORT=3000 HOST=0.0.0.0 API_BASE_URL=http://localhost:8000

COPY . /app
COPY docker/bin/* /usr/bin/
COPY docker/compose/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY docker/compose/nginx/proxy_params /etc/nginx/proxy_params
