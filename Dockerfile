FROM python:3.11-slim

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

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install pydantic-settings

COPY ./src /app/
COPY ./main.py /app/
COPY ./.env /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0",  "--port", "9030"]
