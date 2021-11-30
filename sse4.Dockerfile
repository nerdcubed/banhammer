FROM python:alpine3.10
WORKDIR /app

# Install Requirements
COPY requirements.simd.txt .
RUN apk add --no-cache \
    build-base \
    freetype-dev \
    zlib-dev \
    jpeg-dev && \
  pip install -r requirements.simd.txt && \
  apk del build-base && \
  mkdir output

COPY src/ .
COPY frames.json ./frames.json
COPY assets/ ./assets
COPY frames/ ./frames

ARG GIT_REPO
LABEL org.opencontainers.image.source=${GIT_REPO}

EXPOSE 8080
CMD ["python", "-u", "__main__.py"]
