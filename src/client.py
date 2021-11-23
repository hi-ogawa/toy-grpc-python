import argparse
import asyncio
from typing import Callable, TypeVar

import grpc
from grpc.aio import ClientCallDetails, UnaryUnaryCall

from .protobuf.hello_pb2 import HelloRequest
from .protobuf.hello_pb2_grpc import HelloServiceStub

T = TypeVar("T")


class LogUnaryUnary(grpc.aio.UnaryUnaryClientInterceptor):
    async def intercept_unary_unary(
        self,
        continuation: Callable[[ClientCallDetails, T], UnaryUnaryCall],
        client_call_details: ClientCallDetails,
        request: T,
    ) -> UnaryUnaryCall:
        print("[LogUnaryUnary]", f"{repr(request) = }")
        call = await continuation(client_call_details, request)
        return call


async def main_async(address: str) -> None:
    interceptors = [LogUnaryUnary()]
    channel = grpc.aio.insecure_channel(address, interceptors=interceptors)
    async with channel:
        stub = HelloServiceStub(channel)
        resp = await stub.Hello(HelloRequest(x="hey"))
        print(f"{resp.y = }")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", default="[::]:8080")
    args = parser.parse_args().__dict__
    asyncio.run(main_async(**args))


if __name__ == "__main__":
    main()
