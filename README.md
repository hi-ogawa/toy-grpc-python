# toy-grpc

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

- https://github.com/grpc/grpc/tree/master/src/python/grpcio/grpc/_cython/_cygrpc/aio

```
[Main thread]
grpc.aio.Channel => cygrpc.AioChannel =>
  init_grpc_aio =>
    _actual_aio_initialization (only once) =>
      _initialize_poller =>
        grpc_init
        PollerCompletionQueue =>
          grpc_completion_queue_create_for_next
          threading.Thread(_poll_wrapper) => [Poller thread]
          socket.socketpair (with non-blocking read_socket)
          cpp_event_queue (aka std::queue)
    _initialize_per_loop =>
      PollerCompletionQueue.bind_loop =>
        _BoundEventLoop =>
          Loop.add_reader(read_socket, PollerCompletionQueue._handle_events)
  grpc_insecure_channel_create

Channel.unary_unary => UnaryUnaryMultiCallable.__init__

UnaryUnaryMultiCallable.__call__ => UnaryUnaryCall.__init__ =>
  AioChannel.call => _AioCall => _create_grpc_call =>
    grpc_channel_create_call (with global_completion_queue)
  _invoke (within Loop.create_task) =>
    _common.serialize
    _AioCall.unary_unary =>
      execute_batch (SendMessageOperation, ReceiveMessageOperation, etc...) =>
        Loop.create_future
        CallbackWrapper(future, ...)
        grpc_call_start_batch(grpc_call, ..., CallbackWrapper.c_functor, ...)
          (this call should be relatively cheap and real work is done in `grpc_completion_queue_next` called from "Poller thread")
        await future (see `future.set_result` below)
    _common.deserialize
  _UnaryResponseMixin._init_unary_response_mixin

await UnaryUnaryCall =>
  _UnaryResponseMixin.__await__ (yield above task)


[Main thread read socket handler]
PollerCompletionQueue._handle_events =>
  event = queue.pop()
  CallbackWrapper.functor_run =>
    future.set_result(None) (This resolves `await future` in `execute_batch` above)


[Poller thread]
PollerCompletionQueue._poll_wrapper => _poll =>
  (while loop)
  grpc_completion_queue_next(completion queue)
  queue.push(event)
  _unified_socket_write (notify read socket loop by writing "1" byte)
```

### grpc server runtime

TODO

- https://github.com/grpc/grpc/tree/master/src/python/grpcio/grpc/_cython/_cygrpc/aio

```
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
