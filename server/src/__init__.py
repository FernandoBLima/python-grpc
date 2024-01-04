import grpc
import sys

from concurrent import futures

from src.enums import EnvironmentVariables
from src.service import GRPCModelService
from src.interceptors import RPCIdInterceptor
from src.utils.logging import create_logger, get_root_logger

import model_pb2
import model_pb2_grpc as model_pb2_grpc

logger = create_logger(__name__)

class GRPCServer:
    def __init__(self, host="[::]", port=50051, n_workers=10, interceptors=[], compression=grpc.Compression.Gzip, options=[]) -> None:
        self.server = None
        self.host = host
        self.port = port
        self.n_workers = n_workers 
        self.interceptors = interceptors
        self.compression = compression
        self.server_options = options

    def _init_server(self):
        """
        Function responsible to create a Server with which RPCs can be serviced. 
        """
        self.server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=int(self.n_workers)),
            compression=self.compression,
            interceptors=tuple(interceptors for interceptors in self.interceptors),
            options=self.server_options
        )
        
    async def serve(self):
        """
        Function responsible to tarts this Server and wait and not consume computational resources during blocking
        """
        if not self.server: return
        self.server.add_insecure_port(f"{self.host}:{self.port}")
        await self.server.start()
        await self.server.wait_for_termination()


async def main():
    get_root_logger()

    logger.info('Starting grpc Server...')
    
    try:

        interceptors = [
            RPCIdInterceptor("Interceptor1"),
            RPCIdInterceptor("Interceptor2"),
        ]

        host = EnvironmentVariables.HOST.get_env()
        port = EnvironmentVariables.PORT.get_env()
        n_workers = EnvironmentVariables.N_WORKERS.get_env()

        grpc_instance = GRPCServer(
            host=host, 
            port=port, 
            n_workers=n_workers, 
            interceptors=interceptors
        )
        grpc_instance._init_server()
        model_pb2_grpc.add_GRPCModelServiceServicer_to_server(GRPCModelService(), grpc_instance.server)
        await grpc_instance.serve()

    except Exception as e:
        logger.info('Error: ', e)