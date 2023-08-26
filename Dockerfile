ARG BASE_IMAGE=python:3.10-slim

FROM ${BASE_IMAGE} AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get install -y git g++ python3-dev

WORKDIR /code

COPY requirements.txt /code/BattlePyEngine/
WORKDIR /code/BattlePyEngine

RUN $VIRTUAL_ENV/bin/pip install --upgrade pip && \
        $VIRTUAL_ENV/bin/pip install -r requirements.txt


FROM base AS prod
COPY . /code/BattlePyEngine

RUN $VIRTUAL_ENV/bin/pip install -e .

CMD ["/bin/bash"]

FROM base AS dev
COPY dev_requirements.txt /code/BattlePyEngine/
RUN $VIRTUAL_ENV/bin/pip install -r dev_requirements.txt

COPY . /code/BattlePyEngine
RUN $VIRTUAL_ENV/bin/pip install -e .
