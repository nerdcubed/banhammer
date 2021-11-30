# Banhammer Server
> Exposes an HTTP API for generating GIFs based on Tom Scott's Banhammer

![Example Banhammer GIF](https://i.imgur.com/l1CdgDm.gif)

## Deploying
GitHub Actions builds Docker images automatically. These can be found in this repo's [Container Registry](https://github.com/nerdcubed/banhammer/pkgs/container/banhammer).

There are additional images for systems that support AVX2 and SSE4 which use an alternative image processing system to speed up generation.

## Usage
Simply send a GET request to `/:text` where `:text` is the text you want displayed in the GIF.
The resulting GIF will be returned and cached for at least 20 minutes.

## Renderer
The underlying renderer for the Banhammer GIFs is located at [DerpyChap/banhammer](https://github.com/DerpyChap/banhammer).
