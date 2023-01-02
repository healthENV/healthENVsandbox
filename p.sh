#! /bin/sh

echo "Running commit - \"message $1\"";
git commit --all -m "$1"

git push origin main

echo "Pushing documentation to gh-pages...";
docker compose --file ./docs/Docker-compose_gh_deploy.yml up
echo "End";