#!/bin/bash

echo ${PATH}
# commit the new website version and push it
cd gh-pages; git config user.name "traviscibot"; git config user.email "deploy.well_not_exactly@travis-ci.org"
git add .; git commit --author="${AUTHOR_NAME} <${AUTHOR_EMAIL}>" -m "Deploy ${TRAVIS_COMMIT_RANGE} to github pages"
git push --quiet "https://github.com/${TRAVIS_REPO_SLUG}" gh-pages > /dev/null 2>&1
cd ..
