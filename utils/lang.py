# utils/lang.py

"""Language lookup helpers."""

import discord

from database.service import get_or_create_user, get_or_create_user_from_member


def get_lang_for_member(member: discord.Member) -> str:
    """
    Return the stored language for a guild member, or "en" if none is set.
    """
    user = get_or_create_user_from_member(member)
    return user.language or "en"


def get_lang_for_user(user: discord.abc.User) -> str:
    """
    Return the stored language for a Discord user by ID, or "en" if none is set.
    """
    db_user = get_or_create_user(user.id)
    return db_user.language or "en"
