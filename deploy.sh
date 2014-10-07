#!/bin/bash -xe

git checkout heroku
cd draft
compass compile
cd ..
git add -A .
git commit -a -m 'update assets' || true
git merge -q master >> /dev/null
git push heroku heroku:master --force
git checkout -
