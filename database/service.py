# database/service.py
from contextlib import contextmanager

from typing import List, Optional
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
    """Retrieve an existing user or create a new one by discord_id."""
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=discord_id).first()
        if user is None:
            user = User(discord_id=discord_id)
            db.add(user)
            db.flush()
        return user


def get_or_create_user_from_member(member: Member) -> User:
    """
    Ensure a Member has a user record and refresh username / display_name / is_admin.
    recruit_status is not touched so existing application progress is preserved.
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
    """Return whether the linked user is marked as admin."""
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
    """Refresh username / display_name / is_admin from the member profile."""
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
    """Set recruit status: pending / ready / done."""
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=discord_id).first()
        if user is None:
            user = User(discord_id=discord_id, recruit_status=status)
            db.add(user)
        else:
            user.recruit_status = status

def set_recruit_channels(discord_id: int, text_id: int | None, voice_id: int | None) -> None:
    """Store text and voice channel IDs for the recruit interview channels."""
    with get_session() as db:
        user = db.query(User).filter_by(discord_id=discord_id).first()
        if user is None:
            user = User(discord_id=discord_id)
            db.add(user)

        user.recruit_text_channel_id = text_id
        user.recruit_voice_channel_id = voice_id
        db.flush()


def get_recruit_code(user: User) -> str:
    """Return recruit code based on user ID using the R-0001, R-0002 pattern."""
    return f"R-{user.id:04d}"


def get_recruits_all() -> list[User]:
    """Return all recruits where recruit_status is not NULL."""
    with SessionLocal() as session:
        return (
            session.query(User)
            .filter(User.recruit_status.isnot(None))
            .order_by(User.id)
            .all()
        )

def get_recruits_by_status(status: str) -> list[User]:
    """Return recruits filtered by status: pending / ready / done / rejected."""
    status = (status or "").lower()
    with SessionLocal() as session:
        return (
            session.query(User)
            .filter(User.recruit_status == status)
            .order_by(User.id)
            .all()
        )

def get_user_by_discord_id(discord_id: int) -> Optional[User]:
    """Return a user by discord_id if present."""
    with SessionLocal() as session:
        return (
            session.query(User)
            .filter(User.discord_id == discord_id)
            .one_or_none()
        )

def get_user_by_username(username: str) -> Optional[User]:
    """Return a user by Discord username (e.g., sillygilly3544)."""
    with SessionLocal() as session:
        return (
            session.query(User)
            .filter(User.username == username)
            .one_or_none()
        )
