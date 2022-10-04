# -*- coding: utf-8 -*-
import argparse
import json
from random import choice
from typing import Dict

import grpc
import uvicorn
from fastapi import FastAPI
from google.protobuf.json_format import MessageToJson

import frogs
from definitions.builds.service_pb2_grpc import FrogGivingServiceStub
from definitions.builds.service_pb2 import FrogRequest
from endpoints import grpc_endpoint

router = FastAPI()


@router.get("/health")
def health() -> str:
    """
    Simple healthcheck for Fastapi server
    Returns:
        String "ok"
    """
    return "ok"


@router.get("/generate_frog")
async def generate_frog() -> Dict:
    """
    Generates a frog using GRPC. Picks random gender and continent. And returns a frog.
    Args:

    Returns:
        Frog object encoded as Json. Frog's continent and gender will be random
    """
    with grpc.insecure_channel(grpc_endpoint) as channel:
        client = FrogGivingServiceStub(channel)
        org = client.GetFrog(FrogRequest(gender=choice(list(frogs.names.keys())),
                                         continent=choice(list(frogs.species.keys()))))
        return json.loads(MessageToJson(org, preserving_proto_field_name=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute FastApi server for Frogs")
    parser.add_argument("-p", dest="port", type=int, help="port", default=3001)
    args = parser.parse_args()

    uvicorn.run(router, host='0.0.0.0', port=args.port)
