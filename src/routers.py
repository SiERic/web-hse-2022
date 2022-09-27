from fastapi import APIRouter, Response, status

from src import contracts
from src.repository.meme_repository_impl import MemeRepositoryImpl

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
    mem = repository.get_meme_by_id(id)
    if len(mem) == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"text": f"Meme with id = {id} does not exist"}
    elif len(mem) > 1:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"text": "Multiple record with the same id"}
    else:
        return {"text": mem[0].text}


repository = MemeRepositoryImpl(True)


@router.get("/meme_hashtag/{hashtag_text}")
async def get_memes_by_hashtag(hashtag_text: str, response: Response):
    hashtag_id = repository.get_hashtag_by_text(hashtag_text)
    if len(hashtag_id) == 0:
        return {"memes": []}
    elif len(hashtag_id) > 1:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"text": "Multiple record with the same id"}
    else:
        meme_ids = repository.get_meme_ids_linked_to_hashtag(hashtag_id[0].id)
        memes = repository.get_memes_by_ids(meme_ids)
        return {"memes": list(map(lambda x: x.text, memes))}
