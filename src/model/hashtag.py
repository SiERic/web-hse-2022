from tinydb.table import Document


class Hashtag:
    def __init__(self, id: int, text: str):
        self.id = id
        self.text = text


def document_to_hashtag(document: Document) -> Hashtag:
    return Hashtag(document["id"], document["text"])
