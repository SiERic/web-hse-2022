# -*- coding: utf-8 -*-
import argparse
from time import time

import grpc

from definitions.builds.service_pb2 import Frog, FrogRequest
from definitions.builds.service_pb2_grpc import FrogGivingServiceStub
from endpoints import grpc_endpoint


def request(gender: str, continent: str) -> Frog:
    with grpc.insecure_channel(grpc_endpoint) as channel:
        client = FrogGivingServiceStub(channel)
        return client.GetFrog(FrogRequest(gender=gender, continent=continent))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute FastApi server for Frogs")
    parser.add_argument("-g", dest="gender", type=str, help="gender (Male/Female)", default="Female")
    parser.add_argument("-c", dest="continent", type=str, help="continent", default="Europe")
    args = parser.parse_args()

    print(request(args.gender, args.continent))
