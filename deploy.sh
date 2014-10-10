#!/bin/bash -xe

git branch -D heroku
git checkout -b heroku master
git merge -q heroku_branch_patches >> /dev/null
cd draft
compass compile -e production --force
cd ..
git add -A .
git commit -a -m 'update assets' || true
git merge -q master >> /dev/null
git push heroku heroku:master --force
git checkout -
