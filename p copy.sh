#! /bin/sh

echo "Running commit - \"message $1\"";
git add -a
git commit -m \"$1\"

echo "Pushing documentation to gh-pages...";
git push origin main

echo "End";