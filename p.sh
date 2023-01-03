#! /bin/sh
# TODO: #2 It would be great to have the gh-deploy working within GitHub actions from a Docker container. (difficult to do so far)
echo "Pushing documentation to gh-pages...";
#docker compose --file ./docs/Docker-compose_gh_deploy.yml up

echo "Running commit - \"message $1\"";
#git commit --all -m "$1"
#git push origin main

git add . ;git commit -a -m "$1"

echo "Documents done";