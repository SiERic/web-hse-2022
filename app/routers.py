from fastapi import APIRouter, Response,  status

from app import contracts
from tinydb import Query

from app.db import set_db

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


@router.get("/meme/{id}")
async def get_meme_by_id(id: int, response: Response):
    mem = meme.search(Query()["id"] == id)
    if len(mem) == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"text": f"Meme with id = {id} does not exist"}
    elif len(mem) > 1:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"text": "Multiple record with the same id"}
    else:
        return {"text": mem[0]["text"]}

meme, hashtag, meme_hashtag = set_db()
