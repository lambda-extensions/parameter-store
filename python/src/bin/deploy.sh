#!/bin/bash

set -e

bin/build.sh

aws lambda publish-layer-version \
    --layer-name "lambda-extensions_parameter-store" \
    --region "us-east-1" \
    --zip-file "fileb://extension.zip" \
    --compatible-runtimes python3.8
