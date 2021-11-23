# toy-grpc

TODO

- setup mypy

## Example

```sh
# Setup directories for pyton import path
rm -rf protobuf/out src/protobuf
mkdir -p protobuf/out/src/protobuf
ln -srf protobuf/out/src/protobuf src/protobuf

# Run protoc
python -m grpc_tools.protoc \
  --{python,grpc_python,mypy,mypy_grpc}_out=protobuf/out \
  --proto_path=protobuf/in \
  protobuf/in/src/protobuf/hello.proto

# Run server
python -m src.server

# Run client
python -m src.client

# From cli tool
grpcurl -plaintext -d '{"x": "hey"}' '[::]:8080' 'HelloService/Hello'
```

## Implementation

### grpc client runtime

TODO

```
Channel.unary_unary => UnaryUnaryMultiCallable => UnaryUnaryCall
```

### grpc server runtime

TODO

```
[grpc_aio.pyx]
AioServer.start => ???
```

### protobuf serialization

TODO

- https://github.com/protocolbuffers/protobuf/blob/master/python/google/protobuf/pyext/message.cc

```
Message.SerializeToString
Message.FromString
```

## References

- https://github.com/grpc/grpc/blob/master/src/python/grpcio/README.rst
- https://github.com/grpc/grpc/blob/master/tools/distrib/python/grpcio_tools/README.rst
- https://github.com/protocolbuffers/protobuf/blob/master/python/README.md
- https://github.com/protocolbuffers/protobuf/blob/master/python/google/protobuf/pyext/README
- https://github.com/grpc/grpc/blob/master/examples/python/README.md
