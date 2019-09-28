FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /app/src/

RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.5/community" >> /etc/apk/repositories \
  && apk update \
  && apk add --update-cache --no-cache libgcc libquadmath musl \
  && apk add --update-cache --no-cache libgfortran \
  && apk add --update-cache --no-cache lapack-dev

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
        gcc \
        make \
        musl-dev \
        python3-dev \
        postgresql-dev \
    && apk add  --no-cache --virtual .build-deps-edge \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        gdal-dev \
        geos-dev
RUN apk add --no-cache openssl-dev libffi-dev

COPY requirements.txt /app/
RUN apk add --no-cache \
            --allow-untrusted \
            --repository \
             http://dl-3.alpinelinux.org/alpine/edge/testing \
            hdf5 \
            hdf5-dev && \
    apk add --no-cache \
        build-base
RUN pip install --disable-pip-version-check --no-cache-dir h5py==2.9.0
RUN pip install --disable-pip-version-check --no-cache-dir numpy==1.16.4
RUN pip install --disable-pip-version-check --no-cache-dir pandas==0.24.2

RUN apk add --no-cache --virtual build-dependencies python --update py-pip \
    && apk add --virtual build-runtime \
    gfortran

RUN pip install --disable-pip-version-check --no-cache-dir scipy==1.3.0
RUN pip install --disable-pip-version-check --no-cache-dir pymorphy2==0.8 flask==1.1.1 nltk==3.2.5 Cython==0.29.12 keras==2.2.4 numpy==1.16.4

RUN cd /app/ && \
    pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

COPY src /app/src/
WORKDIR /app/src/


CMD ["gunicorn", "-w", "3", "--bind", ":8000", "config.wsgi:application"]
