from contextlib import contextmanager

from .db import SessionLocal
from .models import User


@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_or_create_user(discord_id: int) -> User:
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=discord_id).first()
        if user is None:
            user = User(discord_id=discord_id)
            db.add(user)
        return user


def set_language(discord_id: int, lang: str) -> None:
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=discord_id).first()
        if user is None:
            user = User(discord_id=discord_id, language=lang)
            db.add(user)
        else:
            user.language = lang


def link_steam(discord_id: int, steam_id: str) -> None:
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=discord_id).first()
        if user is None:
            user = User(discord_id=discord_id, steam_id=steam_id)
            db.add(user)
        else:
            user.steam_id = steam_id
