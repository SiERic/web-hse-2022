from tinydb import TinyDB


def set_db():
    meme = TinyDB("db/meme.json")
    # hashtag = (TinyDB("db/hashtag.json")).table("hashtag")
    # meme_hashtag = (TinyDB("db/meme_hashtag.json")).table("meme_hashtag")
    # return meme.table("meme"), hashtag, meme_hashtag
    return meme.table("meme"), [], []
