from typing import List

from tinydb import where

from src.db import set_db
from src.model.hashtag import Hashtag, document_to_hashtag
from src.model.meme import document_to_meme, Meme
from src.repository.meme_repository import MemeRepository


class MemeRepositoryImpl(MemeRepository):
    def __init__(self, is_prod: bool):
        self.meme_db, self.hashtag_db, self.meme_hashtag_db = set_db(is_prod)

    def get_meme_by_id(self, id: int) -> List[Meme]:
        return list(map((lambda x: document_to_meme(x)), self.meme_db.search(where("id") == id)))

    def get_meme_ids_linked_to_hashtag(self, hashtag_id: int) -> List[int]:
        return list(map((lambda x: x["meme_id"]), self.meme_hashtag_db.search(where("hashtag_id") == hashtag_id)))

    def get_meme_last_id(self) -> int:
        return max(map(lambda x: x["id"], self.meme_db.all()))

    def get_hashtag_last_id(self) -> int:
        return max(map(lambda x: x["id"], self.hashtag_db.all()))

    def get_memes_by_ids(self, meme_ids: List[int]) -> List[Meme]:
        result = []
        for id in meme_ids:
            result.extend(self.get_meme_by_id(id))
        return result

    def link_meme_hashtag(self, meme_id: int, hashtag_id: int) -> None:
        self.meme_hashtag_db.upsert({"meme_id": meme_id, "hashtag_id": hashtag_id}, (where("meme_id") == meme_id) & (where("hashtag_id") == hashtag_id))

    def get_hashtag_by_text(self, text: str) -> List[Hashtag]:
        return list(map((lambda x: document_to_hashtag(x)), self.hashtag_db.search(where("text") == text)))

    def add_meme(self, meme_text: str, hashtags: List[str]):
        new_meme_id = self.get_meme_last_id() + 1
        last_hashtag_id = self.get_hashtag_last_id()
        self.meme_db.insert({"id": new_meme_id, "text": meme_text})
        for hashtag_text in hashtags:
            existing_hashtags = self.get_hashtag_by_text(hashtag_text)
            if len(existing_hashtags) == 0:
                last_hashtag_id += 1
                self.hashtag_db.insert({"id": last_hashtag_id, "text": hashtag_text})
                self.link_meme_hashtag(new_meme_id, last_hashtag_id)
            else:
                for hashtag in existing_hashtags:
                    self.link_meme_hashtag(new_meme_id, hashtag.id)

    def clear_dbs(self) -> None:
        self.meme_db.remove()
        self.hashtag_db.remove()
        self.meme_hashtag_db.remove()
