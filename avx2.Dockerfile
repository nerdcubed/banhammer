FROM python:alpine3.7
WORKDIR /app

# Install Requirements
COPY requirements.simd.txt .
RUN CC="cc -mavx2" apk add --no-cache \
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

EXPOSE 8080
CMD ["python", "-u", "__main__.py"]
