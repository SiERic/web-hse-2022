from tinydb.table import Document


class Meme:
    def __init__(self, id: int, text: str):
        self.id = id
        self.text = text


def document_to_meme(document: Document) -> Meme:
    return Meme(document["id"], document["text"])
