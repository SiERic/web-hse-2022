from pathlib import Path
from tinydb import TinyDB


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def set_db(is_prod: bool):
    if is_prod:
        root = str(get_project_root())
    else:
        root = str(get_project_root()) + "/test"
    meme = TinyDB(root + "/db/meme.json")
    hashtag = TinyDB(root + "/db/hashtag.json")
    meme_hashtag = TinyDB(root + "/db/meme_hashtag.json")
    return meme.table("meme"), hashtag.table("hashtag"), meme_hashtag.table("meme_hashtag")
