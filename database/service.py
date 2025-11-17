from contextlib import contextmanager

from discord import Member

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
    """
    Базовая версия — по одному discord_id.
    Используем там, где у нас нет Member.
    """
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=discord_id).first()
        if user is None:
            user = User(discord_id=discord_id)
            db.add(user)
            db.flush()
        return user


def get_or_create_user_from_member(member: Member) -> User:
    """
    Расширенная версия: есть Member, значит можем
    сразу синхронизировать username / display_name / is_admin.
    """
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=member.id).first()
        if user is None:
            user = User(discord_id=member.id)
            db.add(user)

        # базовые поля из дискорда
        user.username = member.name               # глобальный логин
        user.display_name = member.display_name   # ник на сервере

        # флаг админа по правам гильдии
        user.is_admin = bool(member.guild_permissions.administrator)

        db.flush()
        return user


def user_is_admin(member: Member) -> bool:
    """
    Удобная проверка "ботовского" админа.
    Сейчас просто синхронизируем с правами Discord.
    Потом можно будет заменить на свою логику (ручной флаг, супер-админы и т.п.).
    """
    user = get_or_create_user_from_member(member)
    return bool(user.is_admin)


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


def update_discord_profile(member: Member) -> None:
    """
    Синхронизируем username / display_name / is_admin с БД.
    Можно вызывать при онбординге, при командах и т.п.
    """
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=member.id).first()
        if user is None:
            user = User(discord_id=member.id)
            db.add(user)

        user.username = member.name
        user.display_name = member.display_name
        user.is_admin = bool(member.guild_permissions.administrator)
        db.flush()
