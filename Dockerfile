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

COPY requirements.txt setup.py README.md /code/BattlePyEngine/
WORKDIR /code/BattlePyEngine

RUN $VIRTUAL_ENV/bin/pip install --upgrade pip && \
        $VIRTUAL_ENV/bin/pip install -r requirements.txt

COPY . /code/BattlePyEngine

RUN $VIRTUAL_ENV/bin/pip install -e .

CMD ["/bin/bash"]

FROM base AS dev
RUN $VIRTUAL_ENV/bin/pip install -r dev_requirements.txt
