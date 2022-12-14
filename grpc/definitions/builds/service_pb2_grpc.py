# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import service_pb2 as service__pb2


class FrogGivingServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Health = channel.unary_unary(
                '/FrogGivingService/Health',
                request_serializer=service__pb2.Null.SerializeToString,
                response_deserializer=service__pb2.Null.FromString,
                )
        self.GetFrog = channel.unary_unary(
                '/FrogGivingService/GetFrog',
                request_serializer=service__pb2.FrogRequest.SerializeToString,
                response_deserializer=service__pb2.Frog.FromString,
                )


class FrogGivingServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Health(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFrog(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FrogGivingServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Health': grpc.unary_unary_rpc_method_handler(
                    servicer.Health,
                    request_deserializer=service__pb2.Null.FromString,
                    response_serializer=service__pb2.Null.SerializeToString,
            ),
            'GetFrog': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFrog,
                    request_deserializer=service__pb2.FrogRequest.FromString,
                    response_serializer=service__pb2.Frog.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'FrogGivingService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FrogGivingService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Health(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FrogGivingService/Health',
            service__pb2.Null.SerializeToString,
            service__pb2.Null.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFrog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FrogGivingService/GetFrog',
            service__pb2.FrogRequest.SerializeToString,
            service__pb2.Frog.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
