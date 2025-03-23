# Python grpc server boilerplate
This is well strcutured python grpc server boilerplate.

## Features
* good folder structure
* dockerized
* interceptors for authentication
* proto generate script (protobuf to proto generate)

## Run project steps

### package install with pipenv

> [!NOTE]  
> you need to ensure that you have python `3.12+` installed on your machine and `pipenv` installed

```bash
pipenv shell
pipenv install
```

### serve project

```bash
./run_project.sh
```
this will run grpc server on port 50051

* you can test api with [apidog desktop app](https://apidog.com/)

### docs

* [dockerize script docs](_docs/docker.md)
* [protobuf to proto script docs](_docs/proto-buff.md)
