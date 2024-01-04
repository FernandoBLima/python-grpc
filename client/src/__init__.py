import grpc
import random
import sys
import traceback

from abc import ABCMeta, abstractmethod
from typing import Dict

from src.enums import EnvironmentVariables
from src.services import ClientServices
from src.utils.logging import create_logger, get_root_logger

# sys.path.append('../../') 

import model_pb2
import model_pb2_grpc as model_pb2_grpc

logger = create_logger(__name__)


class BaseGRPCGateway(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "create_channel") and callable(subclass.create_channel)
        ) or NotImplemented

    @abstractmethod
    def create_channel(self, message: Dict):
        """send a message to broker"""


class GRPCClient(BaseGRPCGateway):
    def __init__(self, host="[::]", port=50051, n_workers=10, interceptors=[], compression=grpc.Compression.Gzip, options=[]) -> None:
        self.server = None
        self._grpc_host_grpc = host
        self._grpc_port_grpc = port
        self.n_workers = n_workers 
        self.interceptors = interceptors
        self.compression = compression
        self.server_options = options
        # self.create_channel()

    
    def create_channel(self):
        logger.info(
            f"Predictor channel - port: {self._grpc_host_grpc}, host: {self._grpc_port_grpc}"
        )

        logger.info("Connecting with gRPC server...")
        self._channel = grpc.insecure_channel(
            target=f"{self._grpc_host_grpc}:{self._grpc_port_grpc}",
            # options=self._options
        )
        logger.info("gRPC channel connected!")

async def main():
    get_root_logger()

    logger.info('Starting client...')
    options = []
    options.append(("grpc.enable_retries", 1))

    try:
        host = EnvironmentVariables.HOST.get_env()
        port = EnvironmentVariables.PORT.get_env()
        with grpc.insecure_channel(f'{host}:{port}', options=options, compression=grpc.Compression.Gzip) as channel:
            stub = model_pb2_grpc.GRPCModelServiceStub(channel)

            rpc_id = "{:032x}".format(random.getrandbits(128))
            metadata = grpc.aio.Metadata(("client-rpc-id", rpc_id))

            ClientServices.simple_rpc(stub, metadata)
            ClientServices.request_streaming_method(stub, metadata)
            ClientServices.response_streaming_method(stub, metadata)
            ClientServices.bidirectional_streaming_method(stub, metadata)

    except grpc.RpcError as e:
        logger.debug(f"Exception stacktrace: {traceback.format_exc()}")
    except Exception as e:
        logger.error(e)