# database/service.py
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
    """Базовая версия — только по discord_id."""
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=discord_id).first()
        if user is None:
            user = User(discord_id=discord_id)
            db.add(user)
            db.flush()
        return user


def get_or_create_user_from_member(member: Member) -> User:
    """
    Есть Member → можем сразу обновить username / display_name / is_admin.
    recruit_status тут НЕ трогаем, он управляется рекрутерской логикой.
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
        return user


def user_is_admin(member: Member) -> bool:
    """Проверка админа для логики бота."""
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


def build_steam_url(steam_id: str) -> str:
    return f"https://steamcommunity.com/profiles/{steam_id}"


def link_steam(discord_id: int, steam_id: str) -> None:
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=discord_id).first()
        if user is None:
            user = User(discord_id=discord_id)
            db.add(user)

        user.steam_id = steam_id
        user.steam_url = build_steam_url(steam_id)



def update_discord_profile(member: Member) -> None:
    """Синхронизируем username / display_name / is_admin с БД."""
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=member.id).first()
        if user is None:
            user = User(discord_id=member.id)
            db.add(user)

        user.username = member.name
        user.display_name = member.display_name
        user.is_admin = bool(member.guild_permissions.administrator)
        db.flush()


def set_recruit_status(discord_id: int, status: str) -> None:
    """Меняем статус рекрута: pending / ready / done."""
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=discord_id).first()
        if user is None:
            user = User(discord_id=discord_id, recruit_status=status)
            db.add(user)
        else:
            user.recruit_status = status


def get_recruit_code(user: User) -> str:
    """Генерируем код рекрута по его ID в формате R-0001, R-0002 и т.д."""
    return f"R-{user.id:04d}"
