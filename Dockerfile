FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    bzip2 \
    g++ \
    git \
    graphviz \
    libgl1-mesa-glx \
    libhdf5-dev \
    openmpi-bin \
    libpoppler-dev \
    wget \
    python3-tk && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install poppler-utils -y

ARG APP_HOME="/local/services"
ARG PROJECT_NAME="turnstile"
ARG PROJECT_PATH="${APP_HOME}/${PROJECT_NAME}"
WORKDIR ${PROJECT_PATH}

COPY ./${PROJECT_NAME}/requirements.txt ${PROJECT_PATH}/
RUN pip install -r requirements.txt

ARG env

COPY ./${PROJECT_NAME}/src/ ${PROJECT_PATH}/
COPY ./${PROJECT_NAME}/main.py ${PROJECT_PATH}/
COPY ./${PROJECT_NAME}/.env ${PROJECT_PATH}/
COPY ./${PROJECT_NAME}/properties ${PROJECT_PATH}/properties/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0",  "--port", "9030"]
