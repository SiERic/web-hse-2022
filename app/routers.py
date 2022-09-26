from typing import Optional

from fastapi import APIRouter

from app import contracts

router = APIRouter()


@router.get("/")
async def hello_world():
    return {"message": "Hello World"}


# path parameter

@router.get("/hello/{name}")
async def hello_user(name: str):
    return {"message": f"Hello {name}"}


# query parameters

@router.get("/greeting/")
async def greetings_user(greeting: str, name: str):
    return {"message": f"{greeting} {name}"}


# request body
@router.post("/frog/")
async def get_frog(frog_request: contracts.Frog):
    return {"message": f"Here's your frog named {frog_request.name} of color {frog_request.color}: 🐸"}

