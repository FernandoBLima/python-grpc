import grpc
import random
import sys
import time

from src.utils.logging import create_logger

import model_pb2
import model_pb2_grpc as model_pb2_grpc

CLIENT_ID = 1
logger = create_logger(__name__)


class ClientServices():
    def simple_rpc(stub, metadata=None):
        """
        Function where the client sends a request to the server using the stub and waits for a response to come back, just like a normal function call.

        Args:
        - request (model_pb2.Request)
        - metadata
        """
        list_values = [round(random.uniform(0, 10), 1) for _ in range(4)]
        response = stub.SimpleRPC(
                        model_pb2.Request(
                        client_id=CLIENT_ID, 
                        request_data="called by Python client",
                        float_values = list_values
                    ),
                    metadata=metadata
        )
        logger.info(f"--- Simple RPC response from server {response.server_id}. The message = {response.response_data}")
            

    def request_streaming_method(stub, metadata=None):
        """
        Function where the client sends a request to the server and gets a stream to read a sequence of messages back. 
        The client reads from the returned stream until there are no more messages.
        
        Args:
        - metadata
        """
        try:
            def request_messages():
                for i in range(5):
                    list_values = [round(random.uniform(0, 10), 1) for _ in range(4)]

                    request = model_pb2.Request(
                        client_id=CLIENT_ID,
                        request_data="Message:%d" % i,
                        float_values = list_values
                    )
                    yield request

            response = stub.RequestStreamingMethod(request_messages(), metadata=metadata)
            logger.info(f"--- Request-streaming RPC response from server({response.server_id}) | Mwssage={response.response_data} | Result={response.results_model}")
        except grpc.RpcError as rpc_error:
            logger.error(rpc_error.details(), rpc_error.code(), rpc_error.code().name, rpc_error.code().value)

    def response_streaming_method(stub, metadata=None):
        """
        Function where the client sends a sequence of messages to the server using a provided stream.
        
        Args:
        - metadata
        """
        values = [round(random.uniform(0, 10), 1) for _ in range(4)]

        request = model_pb2.Request(
            client_id=CLIENT_ID, 
            request_data="called by Python client", 
            float_values=values
        )

        response_iterator = stub.ResponseStreamingMethod(request, metadata=metadata)
        for response in response_iterator:
            logger.info(f"--- Response-streaming RPC response from server({response.server_id}) | Message={response.response_data} | Result={response.results_model}")

    def bidirectional_streaming_method(stub, metadata=None):
        """
        Function where the client send a sequence of messages using a read-write stream.
        
        Args:
        - metadata
        """
        def request_messages():
            for i in range(5):
                list_values = [round(random.uniform(0, 10), 1) for _ in range(4)]

                request = model_pb2.Request(
                    client_id=CLIENT_ID,
                    request_data="called by Python client, message: %d" % i,
                    float_values = list_values
                )
                yield request
                time.sleep(1)

        response_iterator = stub.BidirectionalStreamingMethod(request_messages(), metadata=metadata)
        for response in response_iterator:
            logger.info(f"---  bidirectionally-streaming RPC response from server({response.server_id}) | Message={response.response_data} | Result={response.results_model}")
        # except grpc.RpcError as rpc_error:
        #     logger.error(rpc_error.details(), rpc_error.code(), rpc_error.code().name, rpc_error.code().value)