# -*- coding: utf-8 -*-
import collections
import json
from random import choice
import requests

import pytest as pytest

import client
import endpoints
import frogs
import grpc_server


@pytest.mark.unittest
def test_frog_generation() -> None:
    """
        Tests that assigned frogs are coherent with their gender/continent
    """
    count = 2000
    for _ in range(count):
        gender = choice(list(frogs.names.keys()))
        continent = choice(list(frogs.species.keys()))
        frog = grpc_server.Service.PickFrog(gender=gender, continent=continent)
        assert frog.name in frogs.names[gender]
        assert frog.species in frogs.species[continent]


@pytest.mark.unittest
def test_equiprobability() -> None:
    """
        Tests that generation of names/species is equiprobable
    """
    count = 2000
    gender = choice(list(frogs.names.keys()))
    continent = choice(list(frogs.species.keys()))

    names = collections.Counter()
    species = collections.Counter()

    for _ in range(count):
        frog = grpc_server.Service.PickFrog(gender=gender, continent=continent)
        names[frog.name] += 1
        species[frog.species] += 1

    for _, times in dict(names).items():
        expected = count / len(frogs.names[gender])
        assert expected * 0.5 <= times <= expected * 1.5

    for _, times in dict(species).items():
        expected = count / len(frogs.species[continent])
        assert expected * 0.5 <= times <= expected * 1.5


@pytest.mark.functional
def test_grpc_client() -> None:
    """
        Test that gRPC client works properly
    """
    frog = client.request(gender="Male", continent="America")
    assert frog.gender == "Male"
    assert frog.name in frogs.names["Male"]
    assert frog.continent == "America"
    assert frog.species in frogs.species["America"]

    frog = client.request(gender="Female", continent="Australia")
    assert frog.gender == "Female"
    assert frog.name in frogs.names["Female"]
    assert frog.continent == "Australia"
    assert frog.species in frogs.species["Australia"]


@pytest.mark.functional
def test_fastapi_server() -> None:
    """
        Test that main endpoint works properly and generates what is expected
    """
    count = 20
    for _ in range(count):
        r = requests.get(f"http://{endpoints.fastapi_endpoint}/generate_frog").json()
        assert r["gender"] in list(frogs.names.keys())
        assert r["name"] in frogs.names[r["gender"]]
        assert r["continent"] in list(frogs.species.keys())
        assert r["species"] in frogs.species[r["continent"]]
