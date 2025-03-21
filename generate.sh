python -m grpc_tools.protoc -I=protobuf/ --python_out=src/proto --grpc_python_out=src/proto protobuf/*.proto
	cd src/proto && sed -i '' 's/^\(import.*pb2\)/from . \1/g' *.py