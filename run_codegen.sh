#!/usr/bin/env bash

mkdir -p proto/build

python \
    -m grpc.tools.protoc \
    -I. \
    --python_out=proto/build/. \
    --grpc_python_out=proto/build/. \
    proto/search.proto
