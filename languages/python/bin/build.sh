#!/bin/bash

set -e

[ -d build ] && rm -rf build
[ -f extension.zip ] && rm extension.zip

poetry export -f requirements.txt --output requirements.txt

chmod +x extensions/parameter-store-extension
chmod +x parameter-store-extension/extension.py

mkdir -p build/

cp -R extensions build/
cp -R parameter-store-extension build/

pip install -r requirements.txt -t build/parameter-store-extension

cd build; zip -r ../extension.zip *
