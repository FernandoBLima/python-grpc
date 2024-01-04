import contextvars
import grpc

from typing import Awaitable, Callable, Optional

from src.utils.logging import create_logger

rpc_id_var = contextvars.ContextVar("rpc_id", default="default")

logger = create_logger(__name__)

        
class RPCIdInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self, tag: str, rpc_id: Optional[str] = None) -> None:
        self.tag = tag
        self.rpc_id = rpc_id

    async def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        print(f"tag {self.tag} called with rpc_id: {rpc_id_var.get()}")

        if rpc_id_var.get() == "default":
            _metadata = dict(handler_call_details.invocation_metadata)
            rpc_id_var.set(self.decorate(_metadata["client-rpc-id"]))
        else:
            rpc_id_var.set(self.decorate(rpc_id_var.get()))

        return await continuation(handler_call_details)

    def decorate(self, rpc_id: str):
        return f"{self.tag}-{rpc_id}"