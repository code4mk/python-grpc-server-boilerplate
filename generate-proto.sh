#!/bin/sh
# Create output directory if it doesn't exist
mkdir -p src/proto
# Clean existing generated files, except .gitkeep
rm -rf src/proto/*.py src/proto/*.pyc
# Generate proto files
python -m grpc_tools.protoc -I=protobuf/ --python_out=src/proto --grpc_python_out=src/proto protobuf/*.proto
# Fix imports to be relative - using different sed syntax for Linux and MacOS
if [ "$(uname)" = "Darwin" ]; then
    # MacOS
    cd src/proto && sed -i '' 's/^\(import.*pb2\)/from . \1/g' *.py
else
    # Linux
    cd src/proto && sed -i 's/^\(import.*pb2\)/from . \1/g' *.py
fi