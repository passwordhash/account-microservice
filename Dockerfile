FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY src ./src
COPY Makefile ./
COPY .env ./
COPY proto ./proto

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN make generate-keys
RUN make generate-proto

ENV RSA_KEYS_DIR=/app/keys

CMD ["python", "main.py"]
