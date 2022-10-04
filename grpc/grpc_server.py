# -*- coding: utf-8 -*-
import argparse
import random
from concurrent.futures import ThreadPoolExecutor

import grpc

import definitions.builds.service_pb2
from definitions.builds.service_pb2 import FrogRequest, Frog, Null
from definitions.builds.service_pb2_grpc import FrogGivingServiceServicer, add_FrogGivingServiceServicer_to_server

import frogs


class Service(FrogGivingServiceServicer):
    def Health(self, request: Null, context) -> Null:
        """
        Simple healthcheck for service. Always returns Null message.

        Returns:
            Null message
        """
        return request

    @staticmethod
    def PickFrog(gender: str, continent: str) -> Frog:
        """
        Pick random species and name by a given frog
        Args:
            gender: string, Male/Female
            continent: string, any supported continent
        """
        return Frog(name=random.choice(frogs.names[gender]),
                    gender=gender,
                    continent=continent,
                    species=random.choice(frogs.species[continent]))

    def GetFrog(self, request: FrogRequest, context) -> Frog:
        """
        Generates a random frog by a given description (gender and a continent)

        Args:
            request: Object of FrogRequest type. Must contain gender and a continent

        Returns:
            Object of Frog type with name and species fields filled. Species will be coherent with requested continent
        """
        return self.PickFrog(request.gender, request.continent)


def execute_server(port):
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_FrogGivingServiceServicer_to_server(Service(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()

    print("The server is up and running...")
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute GRPC server for Frogs")
    parser.add_argument("-p", dest="port", type=int, help="port", default=3000)
    args = parser.parse_args()

    execute_server(args.port)
