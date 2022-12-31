# README

Simple Dockerfile and Docker-compose to spin up a mkdocs and mkdocstring environment on a ubunutu OS.
To start

> docker compose build
> docker compose up -d
> docker exec -it mkdocs bash
> mkdocs serve --dev-addr=0.0.0.0:8000

You will see document pages at http://localhost:8000