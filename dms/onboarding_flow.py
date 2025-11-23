# dms/onboarding_flow.py
import sys
import discord
from discord.ext import commands

from config import Config
from database.service import (
    set_language,
    get_or_create_user,
    get_or_create_user_from_member,
    update_discord_profile,
    set_recruit_status,
)
from dms.localization import t
from dms.steam_link import SteamLinkView
from dms.recruit_channels import create_recruit_channels
from dms.recruit_moderation import send_recruit_moderation_embed

RECRUIT_ROLE_ID = Config.RECRUIT_ROLE_ID


# ---------- ROLE VIEW ----------


def _get_role_definitions_for_lang(lang: str):
    base = getattr(Config, "ROLE_DEFINITIONS", None)
    eng = getattr(Config, "ROLE_DEFINITIONS_ENG", None)
    rus = getattr(Config, "ROLE_DEFINITIONS_RUS", None)

    if lang == "ru":
        return rus or base or eng or []
    else:
        return eng or base or rus or []


class RoleSelectionView(discord.ui.View):
    """Interactive role selection + recruit registration view."""

    def __init__(self, bot_client: commands.Bot, guild_id: int, lang: str):
        super().__init__(timeout=3600)
        self.bot = bot_client
        self.guild_id = guild_id
        self.lang = lang

        for role_cfg in _get_role_definitions_for_lang(lang):
            self.add_item(RoleButton(role_cfg))

        self.add_item(RegisterRecruitButton())


class RoleButton(discord.ui.Button):
    def __init__(self, role_cfg: dict):
        label = role_cfg.get("label", "Role")
        role_id = role_cfg.get("id", 0)

        super().__init__(
            label=label,
            style=discord.ButtonStyle.secondary,
            custom_id=f"role_{role_id or label}",
        )
        self.role_cfg = role_cfg

    async def callback(self, interaction: discord.Interaction):
        view: RoleSelectionView = self.view  # type: ignore[assignment]
        guild = view.bot.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                "Server not found. Contact staff.",
                delete_after=20,
            )
            return

        role_id = self.role_cfg.get("id")
        if not role_id:
            await interaction.response.send_message(
                "This role is not configured properly.",
                delete_after=20,
            )
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            await interaction.response.send_message(
                "Cannot find your account on this server.",
                delete_after=20,
            )
            return

        role = guild.get_role(role_id)
        if not role:
            await interaction.response.send_message(
                "Role not found. Ask staff to configure it.",
                delete_after=20,
            )
            return

        if role in member.roles:
            await interaction.response.send_message(
                f'Role "{role.name}" is already assigned.',
                delete_after=20,
            )
            return

        try:
            await member.add_roles(role, reason="Self-assigned via onboarding DM")
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to add that role.",
                delete_after=20,
            )
            return

        await interaction.response.send_message(
            f'Role "{role.name}" added!',
            delete_after=20,
        )


# ---------- REGISTER RECRUIT BUTTON ----------


class RegisterRecruitButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Register as Recruit",
            style=discord.ButtonStyle.success,
            custom_id="register_recruit",
        )

    async def callback(self, interaction: discord.Interaction):
        view: RoleSelectionView = self.view  # type: ignore
        guild = view.bot.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                "Server not found right now.",
                delete_after=20,
            )
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            await interaction.response.send_message(
                "Cannot find your member record on this server.",
                delete_after=20,
            )
            return

        user = get_or_create_user_from_member(member)
        lang = user.language or "en"

        status = (user.recruit_status or "pending").lower()
        if status in ("ready", "done"):
            await interaction.response.send_message(
                "You have already applied as a recruit. Contact staff if something is wrong."
                if lang == "en"
                else "Ты уже зарегистрирован как рекрут. Если что-то не так, напиши рекрутеру.",
                ephemeral=True,
            )
            return

        if getattr(user, "recruit_text_channel_id", None) or getattr(user, "recruit_voice_channel_id", None):
            await interaction.response.send_message(
                "You have already applied as a recruit. Contact staff if something is wrong."
                if lang == "en"
                else "Ты уже зарегистрирован как рекрут. Если что-то не так, напиши рекрутерам.",
                ephemeral=True,
            )
            return

        if not user.steam_id:
            await interaction.response.send_message(
                t(lang, "steam_link"),
                ephemeral=True,
            )
            return

        recruit_id = RECRUIT_ROLE_ID
        if not recruit_id:
            await interaction.response.send_message(
                "Recruit role ID is not configured correctly.",
                delete_after=20,
            )
            return

        recruit_role = guild.get_role(recruit_id)
        if not recruit_role:
            await interaction.response.send_message(
                "Recruit role not found. Ask staff to configure it.",
                delete_after=20,
            )
            return

        if recruit_role in member.roles:
            await interaction.response.send_message(
                "You are already registered as a recruit.",
                delete_after=20,
            )
            return

        try:
            await member.add_roles(recruit_role, reason="Recruit registration")
        except discord.Forbidden:
            await interaction.response.send_message(
                "I cannot grant the recruit role. Contact staff.",
                delete_after=20,
            )
            return

        set_recruit_status(member.id, "ready")

        try:
            text_ch, voice_ch = await create_recruit_channels(guild, member)
        except Exception as e:
            print(f"[recruit channels ERROR] {type(e).__name__}: {e}", file=sys.stderr)
            await interaction.response.send_message(
                "Recruit role assigned, but interview channels could not be created. "
                "Please contact staff.",
                ephemeral=True,
            )
            return

        await send_recruit_moderation_embed(
            guild=guild,
            member=member,
            text_ch=text_ch,
            voice_ch=voice_ch,
        )

        await interaction.response.send_message(
            (
                f'Recruit role "{recruit_role.name}" assigned!\n'
                f'Your application status: **READY**.\n\n'
                f'A private interview text & voice channel have been created for you:\n'
                f'- Text: {text_ch.mention}\n'
                f'- Voice: {voice_ch.mention}'
            ),
            ephemeral=True,
        )


# ---------- LANGUAGE SELECT ----------


class LanguageSelectView(discord.ui.View):
    """First step: language selection."""

    def __init__(self, bot_client: commands.Bot, guild_id: int):
        super().__init__(timeout=900)
        self.bot = bot_client
        self.guild_id = guild_id
        self.add_item(LanguageButton("en", "English"))
        self.add_item(LanguageButton("ru", "Русский"))


class LanguageButton(discord.ui.Button):
    def __init__(self, code: str, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.code = code

    async def callback(self, interaction: discord.Interaction):
        view: LanguageSelectView = self.view  # type: ignore[assignment]

        set_language(interaction.user.id, self.code)

        await interaction.response.send_message(
            t(self.code, "language_set"),
            ephemeral=True,
        )

        guild = view.bot.get_guild(view.guild_id)
        if guild is None:
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            try:
                member = await guild.fetch_member(interaction.user.id)
            except discord.DiscordException:
                return

        await send_role_and_steam_dms(bot=view.bot, member=member, lang=self.code)


# ---------- DM HELPERS ----------


def _format_role_list(lang: str) -> str:
    defs = _get_role_definitions_for_lang(lang)
    if not defs:
        return "- No self-assignable roles are configured."

    lines = []
    for cfg in defs:
        label = cfg.get("label", "Role")
        desc = cfg.get("description", "")
        lines.append(f"- {label}: {desc}".rstrip())
    return "\n".join(lines)


def _build_onboarding_message(member: discord.Member, lang: str) -> str:
    return (
        f"{t(lang, 'greeting').format(name=member.display_name)}\n\n"
        f"{Config.WELCOME_MESSAGE_ENG if lang == 'en' else Config.WELCOME_MESSAGE_RUS}\n\n"
        f"{t(lang, 'roles_header')}\n"
        f"{_format_role_list(lang)}\n\n"
        f"{t(lang, 'roles_hint')}\n\n"
        f"{t(lang, 'recruit_hint')}\n"
    )


def _build_steam_message(member: discord.Member, lang: str) -> str:
    return t(lang, "steam_intro")


async def send_role_and_steam_dms(bot: commands.Bot, member: discord.Member, lang: str):
    await member.send(
        _build_onboarding_message(member, lang),
        view=RoleSelectionView(bot_client=bot, guild_id=member.guild.id, lang=lang),
    )

    await member.send(
        _build_steam_message(member, lang),
        view=SteamLinkView(),
    )


async def send_onboarding_dm(bot: commands.Bot, member: discord.Member) -> bool:
    if member.bot or member.guild is None:
        return True

    try:
        get_or_create_user(member.id)
        update_discord_profile(member)

        text = f"{t('ru', 'choose_language')} / {t('en', 'choose_language')}"

        await member.send(
            text,
            view=LanguageSelectView(bot_client=bot, guild_id=member.guild.id),
        )
        return True
    except discord.Forbidden:
        return False
    except discord.HTTPException as e:
        print(f"Failed to send DM: {e}", file=sys.stderr)
        return False


async def notify_dm_disabled(bot: commands.Bot, member: discord.Member):
    chan_id = Config.FALLBACK_CHANNEL_ID
    if not chan_id:
        return

    channel = bot.get_channel(chan_id)
    if channel is None:
        try:
            channel = await bot.fetch_channel(chan_id)
        except Exception as e:
            print(f"Cannot fetch fallback channel: {e}", file=sys.stderr)
            return

    await channel.send(
        f"{member.mention}, enable direct messages so I can send your onboarding instructions. "
        f"After this, please send the `!onboarding` command on the server."
    )
