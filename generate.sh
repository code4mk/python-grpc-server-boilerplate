# Create output directory if it doesn't exist
mkdir -p src/proto
# Clean existing generated files, except .gitkeep
rm -rf src/proto/*.py src/proto/*.pyc
# Generate proto files
python -m grpc_tools.protoc -I=protobuf/ --python_out=src/proto --grpc_python_out=src/proto protobuf/*.proto
# Fix imports to be relative
cd src/proto && sed -i '' 's/^\(import.*pb2\)/from . \1/g' *.py