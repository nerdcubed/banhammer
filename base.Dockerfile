FROM python:alpine3.10
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

COPY src/ .

ARG GIT_REPO
LABEL org.opencontainers.image.source=${GIT_REPO}

EXPOSE 8080
CMD ["python", "-u", "__main__.py"]
