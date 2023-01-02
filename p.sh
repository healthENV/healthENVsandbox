#! /bin/sh

echo "Pushing documentation to gh-pages...";
docker compose --file ./docs/Docker-compose_gh_deploy.yml up

#echo "Running commit - \"message $1\"";
git commit --all -m "$1"
git push origin main

echo "Documents done";