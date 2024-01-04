# Python-gRPC

## About the Repository

The objective of this repository was to understand gRPC in Python with a practical application. It showcases the integration of a basic SVC model from the sklearn library, utilizing RPC services like Simple, Response Streaming, Request Streaming, and Bidirectional Streaming. Through these implementations, the goal was to provide a hands-on experience in leveraging gRPC's functionalities within Python applications.

## Dependencies

* Python 3.9 or higher
* Other dependencies, check the `requirements.txt` file

## Installation and Start

To install the project's dependencies, run the command below:
On windows you will need to start manually

```powershell
python -m venv venv 
venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pre-commit install
pre-commit autoupdate
pip install -r requirments.txt
```

If you are on Linux or MacOs, you can use the make command to bring up the development environment.

```bash
make venv 
```

### Using Docker Compose 
You will need Docker installed to follow the next steps. To create and run the image use the following command:

```bash
docker-compose up --build
```

The configuration will create a cluster with 2 containers:
- server container
- client container

Another way to run the application without using docker is run the following commands:
```powershell
python client/app.py
python server/app.py
```

## Protos

### Generate protocols

Protocol Buffers compiler can be generate using the following command:

```sh
  python -m grpc_tools.protoc -I ./protos --python_out=. --grpc_python_out=. ./protos/model.proto
```

| Command/Argument              | Description                                                                                                |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `python -m grpc_tools.protoc` | Start Protocol Buffers compiler in the gRPC package.                                                       |
| `-I./protobufs`               | Input directory. The compiler will search this directory for imports. `.` (dot) implies current directory. |
| `--python_out=codegen/`       | Prepare Python classes for Protocol Buffers message types. Save the classes in the folder `codegen/`.      |
| `--grpc_python_out=codegen/`  | Prepare artifacts for the server and the client. Save the code in the folder `codegen/`.                   |
| `model.proto`                 | Path to the .proto file.                                                                                   |


## Project Structure
Below is a project structure created:

```cmd
.
├── README.md
├── docker-compose.yml
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
├── requirements.txt
├── setup.py
├───client/
│   ├───app.py
│   └───src
│       ├───service.py
│       └───utils/
│           └───logging.py
├───pb2/
│   ├───model_pb2_grpc.py
│   ├───model_pb2.py
│   └───model_pb2.pyi
├───protos/
│   └───model.proto
└───server/
    ├───app.py
    └───src
        ├───interceptors.py
        ├───model.py
        ├───service.py
        └───utils/
            └───logging.py
```

## TODO

The following improvements are planned as part of the TODO list for this repository:

  - Add Authentication
  - Add Error Handling
  - Add Health Checking
  - Add Retry Mechanism
  - Create New Interceptors 

These improvements aim to add layers of security, robustness, and monitoring capabilities in the gRPC application, while also extending its functionalities with additional interceptors for improved customization and control over the communication flow.

## Help and Resources
You can read more about the tools documentation:

- [gRPC](https://grpc.io/)
