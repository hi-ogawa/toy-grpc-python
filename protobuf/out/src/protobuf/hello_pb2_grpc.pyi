"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc
import src.protobuf.hello_pb2

class HelloServiceStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    Hello: grpc.UnaryUnaryMultiCallable[
        src.protobuf.hello_pb2.HelloRequest,
        src.protobuf.hello_pb2.HelloResponse] = ...


class HelloServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def Hello(self,
        request: src.protobuf.hello_pb2.HelloRequest,
        context: grpc.ServicerContext,
    ) -> src.protobuf.hello_pb2.HelloResponse: ...


def add_HelloServiceServicer_to_server(servicer: HelloServiceServicer, server: grpc.Server) -> None: ...
