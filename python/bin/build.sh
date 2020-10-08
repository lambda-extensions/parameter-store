#!/bin/bash

set -e

[ -d build ] && rm -rf build
[ -f extension.zip ] && rm extension.zip

pipenv lock -r > requirements.txt
pip install -r requirements.txt -t build

chmod +x extensions/parameter-store-extension
chmod +x parameter-store-extension/extension.py

mkdir -p build/

cp -R extensions build/
cp -R parameter-store-extension build/

cd build; zip -r ../extension.zip *
