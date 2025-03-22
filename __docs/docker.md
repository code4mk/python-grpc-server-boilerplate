# Build the docker image
./docker-image-build.sh

# Run the docker image
docker run -d -it -p 50051:50051 the-grpc-app:1.0.0