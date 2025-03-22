# Use build argument to set Python version, default is 3.12-slim
ARG PYTHON_VERSION=3.12-slim

# Base image with configurable Python version
FROM python:${PYTHON_VERSION}

# Prevent Python from writing pyc files to save disk space
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python outputs everything that's printed inside it without buffering
ENV PYTHONUNBUFFERED 1
# Ignore pipenv warnings about being root user
ENV PIP_ROOT_USER_ACTION ignore

# Install system dependencies needed for grpc and protobuf
# RUN apt-get update && apt-get install -y \
#     protobuf-compiler \
#     && rm -rf /var/lib/apt/lists/*


# Set the working directory for subsequent commands
WORKDIR /var/www/app

# Copy Pipfile and Pipfile.lock to the working directory
COPY Pipfile .
COPY Pipfile.lock .

# Install pipenv using Python's package manager
RUN python3 -m pip install pipenv

# Install Python dependencies defined in Pipfile.lock using pipenv
RUN pipenv install --ignore-pipfile

# Generate protobuf files before copying the rest of the application
COPY protobuf/ ./protobuf/
COPY generate-proto.sh .
RUN mkdir -p src/proto && \
    chmod +x generate-proto.sh && \
    pipenv run ./generate-proto.sh

# Copy the entire application code to the working directory
COPY . .


# Expose port 50051 for the application
EXPOSE 50051

# Command to start the application using pipenv
CMD ["pipenv", "run", "python3", "src/main.py"]