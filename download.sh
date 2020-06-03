#!/bin/bash

if ! [ -e web ]; then
  git clone https://github.com/jakkdu/jakkdu.github.io web
fi

cd web
git checkout pelican
git pull


