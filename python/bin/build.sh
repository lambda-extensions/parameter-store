#!/bin/bash

set -e

[ -d build ] && rm -rf build
[ -f extension.zip ] && rm extension.zip

pipenv lock -r > requirements.txt
pip install -r requirements.txt -t build

chmod +x extensions/parameter-store-extension
chmod +x parameter-store-extension/extension.py

mkdir -p build/opt/extensions

cp -R extensions build/opt/
cp -R parameter-store-extension build/opt/

zip -r extension.zip build

aws lambda publish-layer-version \
    --layer-name "lambda-extensions_parameter-store" \
    --region "us-east-1" \
    --zip-file "fileb://extension.zip"
