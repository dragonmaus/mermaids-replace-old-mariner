#!/bin/sh

name=$(jq -r .Name manifest.json)

git ls-files \
| grep -v '^\.bin/' \
| tr '\n' '\0' \
| xargs -0 \
  git archive \
    --format=zip \
    --prefix="[CP] $name/" \
    "$1"
