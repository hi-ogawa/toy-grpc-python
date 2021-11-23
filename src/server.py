import argparse
import asyncio

import grpc
from grpc_reflection.v1alpha import reflection

from .protobuf.hello_pb2 import DESCRIPTOR, HelloRequest, HelloResponse
from .protobuf.hello_pb2_grpc import (
    HelloServiceServicer,
    add_HelloServiceServicer_to_server,
)

SERVICE_NAMES = (
    reflection.SERVICE_NAME,
    *(service.full_name for service in DESCRIPTOR.services_by_name.values()),
)


class HelloServiceServicerImpl(HelloServiceServicer):
    async def Hello(
        self, req: HelloRequest, _context: grpc.aio.ServicerContext
    ) -> HelloResponse:
        y = f"x = {req.x}"
        return HelloResponse(y=y)


async def main_async(address: str) -> None:
    server = grpc.aio.server()
    add_HelloServiceServicer_to_server(HelloServiceServicerImpl(), server)
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(address)
    print(f"Server listening at {address}")
    await server.start()
    await server.wait_for_termination()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", default="[::]:8080")
    args = parser.parse_args().__dict__
    asyncio.run(main_async(**args))


if __name__ == "__main__":
    main()
