# Tom Scott Banhammer Generator
_Generates GIFs based on Tom Scott's Banhammer_

![](https://safe.n3s.co/hNwoO47U.gif)

## Deploying
GitLab builds this project into a Docker Image, available on the [Container Registry](https://gitlab.com/nerd3-servers/banhammer-generator/container_registry).  
There are additional images for systems that support AVX2 and SSE4 which use an alternative image processing system to speed up generation.

## API Routes
```
GET /api/v1.0/banhammer/:name
```
