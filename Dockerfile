FROM python:alpine3.6
WORKDIR /app

# Install Requirements
COPY requirements.txt .
RUN apk add --no-cache \
    build-base \
    freetype-dev \
    zlib-dev \
    jpeg-dev && \
  pip install -r requirements.txt && \
  apk del build-base

RUN mkdir output

COPY src/ .
COPY frames.json ./frames.json
COPY assets/ ./assets
COPY frames/ ./frames

CMD ["python", "-u", "__main__.py"]
