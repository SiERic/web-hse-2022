from pathlib import Path

import pytest

from src.repository.meme_repository_impl import MemeRepositoryImpl

repository = MemeRepositoryImpl(False)


def get_project_root() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture(autouse=True)
def add_content_to_db():
    root = str(get_project_root()) + "/test"

    f_meme = open(root + "/db/meme.json", 'w')
    f_hashtag = open(root + "/db/hashtag.json", 'w')
    f_meme_hashtag = open(root + "/db/meme_hashtag.json", 'w')
    print('''
{
  "meme": {
    "1": {
      "id": 1,
      "text": "Глава днр Денис Пушилин издал закон, запрещающий менять местами первые буквы его имени и фамилии"
    },
    "2": {
      "id": 2,
      "text": "Знаете, почему нет обзоров на наркотики? Потому что в этой области нет независимых экспертов"
    },
    "3": {
      "id": 3,
      "text": "Если бы мне предложили синюю и красную таблетки, я бы выбрад красную, потому что, скорее всего, это Нурофен экспресс форте"
    },
    "4":{
      "id": 4,
      "text": "Дорогая, а кто эти мы, о которых ты пишешь в своём дипломе"
    }
  }
}
    ''', file=f_meme)
    print('''
{
  "hashtag": {
    "1": {"id": 1, "text": "твиттер"},
    "2": {"id": 2, "text": "наркотики"},
    "3": {"id": 3, "text": "каламбур"},
    "4": {"id": 4, "text": "дорогая"},
    "5": {"id": 5, "text": "диплом"},
    "6": {"id": 6, "text": "нурофен"}
  }
}
    ''', file=f_hashtag)
    print('''
{
  "meme_hashtag": {
    "1": {"meme_id": 1, "hashtag_id": 1},
    "2": {"meme_id": 1, "hashtag_id": 3},
    "3": {"meme_id": 2, "hashtag_id": 1},
    "4": {"meme_id": 2, "hashtag_id": 2},
    "5": {"meme_id": 2, "hashtag_id": 3},
    "6": {"meme_id": 4, "hashtag_id": 1},
    "7": {"meme_id": 4, "hashtag_id": 4},
    "8": {"meme_id": 4, "hashtag_id": 5},
    "9": {"meme_id": 3, "hashtag_id": 6}
  }
}
    ''', file=f_meme_hashtag)


def test_get_meme():
    memes = repository.get_meme_by_id(1)
    assert len(memes) == 1
    assert memes[
               0].text == "Глава днр Денис Пушилин издал закон, запрещающий менять местами первые буквы его имени и фамилии"


def test_meme_number():
    assert repository.get_meme_last_id() == 4


def test_hashtag_number():
    assert repository.get_hashtag_last_id() == 6


def test_get_memes_by_hashtag():
    assert sorted(repository.get_meme_ids_linked_to_hashtag(1)) == [1, 2, 4]
    assert sorted(repository.get_meme_ids_linked_to_hashtag(2)) == [2]
    assert sorted(repository.get_meme_ids_linked_to_hashtag(7)) == []


def test_add_and_get_meme():
    text = '''
— В России отменён масочный режим.
— И введён тоталитарный.
— Что?
— Что?'''
    repository.add_meme(text, ["твиттер", "каламбур", "политика"])
    assert repository.get_meme_by_id(5)[0].text == text
    hashtag = repository.get_hashtag_by_text("политика")[0]
    assert hashtag.text == "политика"
    assert repository.get_meme_ids_linked_to_hashtag(hashtag.id) == [5]
