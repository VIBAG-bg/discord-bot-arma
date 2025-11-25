# dms/recruit_channels.py
import asyncio
import sys
import discord

from config import Config
from database.service import (
    get_or_create_user_from_member,
    get_recruit_code,
    set_recruit_channels,
)

_active_locks: dict[int, asyncio.Lock] = {}


async def ensure_recruit_channels(
    guild: discord.Guild,
    member: discord.Member,
) -> tuple[discord.TextChannel, discord.VoiceChannel]:
    """
    Гарантированно получить (или создать) пару каналов рекрута.
    Защищено локом от одновременных вызовов для одного пользователя.
    """
    user = get_or_create_user_from_member(member)
    lock = _active_locks.setdefault(user.discord_id, asyncio.Lock())

    async with lock:
        user = get_or_create_user_from_member(member)
        text_ch = None
        voice_ch = None

        if getattr(user, "recruit_text_channel_id", None):
            ch = guild.get_channel(user.recruit_text_channel_id)
            if isinstance(ch, discord.TextChannel):
                text_ch = ch

        if getattr(user, "recruit_voice_channel_id", None):
            ch = guild.get_channel(user.recruit_voice_channel_id)
            if isinstance(ch, discord.VoiceChannel):
                voice_ch = ch

        # если оба канала живые — просто возвращаем
        if text_ch and voice_ch:
            return text_ch, voice_ch

        # иначе создаём с нуля (эта функция уже пишет ID в БД)
        text_ch, voice_ch = await create_recruit_channels(guild, member)
        return text_ch, voice_ch



async def create_recruit_channels(
    guild: discord.Guild,
    member: discord.Member,
) -> tuple[discord.TextChannel, discord.VoiceChannel]:
    """
    Создаём личный текстовый и голосовой каналы для рекрута.
    Возвращаем (text_channel, voice_channel).
    """
    category = guild.get_channel(Config.RECRUIT_CATEGORY_ID)
    if category is None or not isinstance(category, discord.CategoryChannel):
        raise RuntimeError("Recruit category is not configured correctly.")

    overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(
            view_channel=True,
            read_message_history=True,
            send_messages=True,
            connect=True,
            speak=True,
        ),
    }

    for role_id in getattr(Config, "RECRUITER_ROLE_IDS", []):
        role = guild.get_role(role_id)
        if role is not None:
            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=True,
                connect=True,
                speak=True,
            )

    user = get_or_create_user_from_member(member)
    code = get_recruit_code(user)

    base_name = f"recruit-{member.name.lower()}-{code}"

    text_channel = await guild.create_text_channel(
        name=base_name,
        category=category,
        overwrites=overwrites,
        reason=f"Recruit interview channel for {member}",
    )

    voice_channel = await guild.create_voice_channel(
        name=base_name,
        category=category,
        overwrites=overwrites,
        reason=f"Recruit interview voice for {member}",
    )

    set_recruit_channels(
        discord_id=member.id,
        text_id=text_channel.id,
        voice_id=voice_channel.id,
    )

    return text_channel, voice_channel
