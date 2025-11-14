# Docker Setup for AngularQuiz Frontend

This document provides instructions for building and running the AngularQuiz frontend using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, for running with backend)

## Quick Start

### Build the Docker Image

```bash
docker build -t quiz-frontend .
```

### Run the Container

```bash
docker run -p 4200:80 quiz-frontend
```

The application will be available at `http://localhost:4200`

## Advanced Usage

### Run in Detached Mode

```bash
docker run -d -p 4200:80 --name quiz-app quiz-frontend
```

### Stop the Container

```bash
docker stop quiz-app
docker rm quiz-app
```

### View Container Logs

```bash
docker logs quiz-app
```

## Building with Docker Compose

From the repository root directory:

```bash
# Build and start both frontend and backend
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# Stop services
docker-compose down
```

## Troubleshooting

### Network Issues During Build

If you experience network connectivity issues during `npm install` in the Docker build:

1. Install dependencies locally first:
   ```bash
   npm install
   ```

2. Comment out `node_modules` in `.dockerignore`:
   ```
   # node_modules
   ```

3. Rebuild the Docker image:
   ```bash
   docker build -t quiz-frontend .
   ```

This will copy your local `node_modules` into the Docker image, bypassing the need for network access during the build.

### Production Build Issues

The Dockerfile uses production configuration with font optimization disabled to avoid network dependency during builds. If you need to modify build settings, edit `angular.json`.

## Docker Image Details

- **Base Image (Build)**: `node:20-alpine`
- **Base Image (Runtime)**: `nginx:alpine`
- **Build Type**: Multi-stage build
- **Image Size**: ~53MB
- **Port**: 80 (mapped to 4200 on host)

## Configuration

The nginx server is configured with:
- Gzip compression
- Static asset caching (1 year)
- Security headers (X-Frame-Options, X-Content-Type-Options, X-XSS-Protection)
- Angular routing support (single-page application)

To customize nginx configuration, edit `nginx.conf` before building the image.

## Environment Variables

Currently, the application doesn't use environment variables. If you need to configure API endpoints or other settings, you can:

1. Use build arguments in the Dockerfile
2. Mount a configuration file at runtime
3. Use nginx environment variable substitution

Example with build arguments:

```dockerfile
ARG API_URL=http://localhost:5000
ENV API_URL=$API_URL
```

Then build with:

```bash
docker build --build-arg API_URL=https://api.example.com -t quiz-frontend .
```
