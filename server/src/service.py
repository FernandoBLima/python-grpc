import sys
import contextvars
import grpc

from src.model import Model
from src.utils.logging import create_logger

# sys.path.append('../../') 
import model_pb2
import model_pb2_grpc as model_pb2_grpc

SERVER_ID = 1
rpc_id_var = contextvars.ContextVar("rpc_id", default="default")
logger = create_logger(__name__)


# rich_status = create_greet_limit_exceed_error_status(
#     request.client_id
# )
# context.set_details("Ouch!")
# context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
# return model_pb2.Response()

class GRPCModelService(model_pb2_grpc.GRPCModelServiceServicer):

    def __init__(self):
        self.model_instance = Model()
        self.model_instance.get_model()

    async def SimpleRPC(self, request: model_pb2.Request, context: grpc.aio.ServicerContext) -> model_pb2.Response:
        """
        Function where the client sends a request to the server using the stub and waits for a response to come back, just like a normal function call.

        Args:
        - request (model_pb2.Request)
        - context:

        Returns:
        - model_pb2.Response:
            - int: server_id: ID do servidor (int64).
            - str: response_data: Dados da resposta (string).
            - List[str]: results_model: Lista de modelos de resultados (repeated string).
        """
        logger.info("#### Simple RPC request called by client ####")
        logger.info(f"SimpleRPC called by client({request.client_id}) | message = {request.request_data} | float_values = {request.float_values}")

        response_data = self.model_instance.get_inference([request.float_values])

        response = model_pb2.Response(
            server_id=SERVER_ID,
            response_data=self.model_instance.target_names[int(response_data)],
        )
        return response


    def RequestStreamingMethod(self, request_iterator: [model_pb2.Request], context: grpc.ServicerContext) -> model_pb2.Response:
        """
        Function where the client sends a request to the server and gets a stream to read a sequence of messages back. The client reads from the returned stream until there are no more messages.

        Args:
        - request_iterator (model_pb2.Request)
        - context:

        Returns:
        - float: Área calculada do retângulo.
        """
        logger.info("#### Request Streaming called by client ####")
        results = []

        for request in request_iterator:
            logger.info(f"Request-Streaming from client({request.client_id}) | message= {request.request_data} | float_values = {request.float_values}")
            response_data = self.model_instance.get_inference([request.float_values])
            result = self.model_instance.target_names[int(response_data)]
            results.append(result)

        response = model_pb2.Response(
            server_id=SERVER_ID,
            response_data="ClientStreamingMethod is ok!",
            results_model=results
        )
        return response

    def ResponseStreamingMethod(self, request: model_pb2.Request, context) -> model_pb2.Response:
        """
        Function where the client writes a sequence of messages and sends them to the server, again using a provided stream.

        Args:
        - request (model_pb2.Request)
        - context:

        Returns:
        - model_pb2.Response:
            - int: server_id: ID do servidor (int64).
            - str: response_data: Dados da resposta (string).
            - List[str]: results_model: Lista de modelos de resultados (repeated string).
        """
        logger.info("#### Response Streaming called by server ####")
        logger.info(f"ResponseStreaming from client({request.client_id}) | message = {request.request_data} | float_values = {request.float_values}")

        def response_messages():
            list_values = range(len(request.float_values))
            for index in list_values:
                response_data = self.model_instance.get_inference([request.float_values])

                response = model_pb2.Response(
                    server_id=SERVER_ID,
                    response_data=f"ServerStreamingMethod is ok, message={str(index)}",
                    results_model=[self.model_instance.target_names[int(response_data)]]
                )
                yield response

        return response_messages()

    def BidirectionalStreamingMethod(self, request_iterator: [model_pb2.Request], context) -> model_pb2.Response:
        """
        Function where both sides send a sequence of messages using a read-write stream.
        
        Args:
        - request_iterator (model_pb2.Request)
        - context:

        Returns:
        - model_pb2.Response:
            - int: server_id: ID do servidor (int64).
            - str: response_data: Dados da resposta (string).
            - List[str]: results_model: Lista de modelos de resultados (repeated string).
        """
        logger.info("#### Bidirectionally-Streaming RPC called by client ####")

        results = []
        i = 0

        for request in request_iterator:
            logger.info(f"Bidirectionally-Streaming from client({request.client_id}) | message= {request.request_data} | float_values = {request.float_values}")
            response_data = self.model_instance.get_inference([request.float_values])
            result = self.model_instance.target_names[int(response_data)]
            results.append(result)

            yield model_pb2.Response(
                server_id=SERVER_ID,
                response_data="Message= %d" % i,
                results_model=[results[i]]
            )
            i = i + 1

        logger.info(results)
