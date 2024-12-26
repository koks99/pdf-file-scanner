# Python Program to Scan PDF files

## Table of Contents

- [Description](#Description)
- [Setup](#Setup)
- [Usage](#Usage)
- [Misc](#Misc)

## Description
This project is a python program powered by FastAPI which helps in extracting and storing metadata from a pdf file with Docker for making it platform-agnostic.

## Setup

### Prerequisites:

Ensure that you have the following installed before proceeding with the setup:
1. Docker and Docker Compose (OR)
2. Docker Desktop application

### Docker build:

```sudo docker-compose build```

## Usage

### Running the Application
1. Spin up the application using this command:
>```sudo docker-compose up```
2. Go to this endpoint using a browser: http://0.0.0.0:8000/docs
3. There, you can see the endpoints available (scan, lookup, image)
4. Use scan to upload the pdf file that needs to be stored.
5. Once successful, you will get back SHA256 hash as response, which be used to lookup the file metadata using `/lookup` and the pdf as an image using `/image`.

## Misc

### Troubleshooting
- If any expected errors are thrown while building the docker image, running this command could help:
```sudo rm  ~/.docker/config.json```
- If you notice orphan containers being created, try using the `--project-name` flag in Docker Compose to avoid multiple containers for the same project.