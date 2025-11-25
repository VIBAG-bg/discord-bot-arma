# dms/onboarding_flow.py

import sys
import discord
from discord.ext import commands

from config import Config
from dms.localization import t
from dms.steam_link import LinkSteamButton, SteamLinkView
from dms.recruit_channels import ensure_recruit_channels
from dms.recruit_moderation import RecruitModerationView
from database.service import (
    get_or_create_user,
    get_or_create_user_from_member,
    set_language,
    update_discord_profile,
    set_recruit_status,
    get_recruit_code,
)

RECRUIT_ROLE_ID = Config.RECRUIT_ROLE_ID


# --------- ВСПОМОГАТЕЛЬНОЕ ---------


def _get_game_role_definitions():
    """Берём игровые роли из конфига, но не падаем, если их нет."""
    return getattr(Config, "GAME_ROLE_DEFINITIONS", []) or []


def _build_onboarding_embed(member: discord.Member, lang: str) -> discord.Embed:
    """Главное приветственное сообщение после выбора языка."""
    greeting = t(lang, "greeting").format(name=member.display_name)
    body = t(lang, "onboarding_body")
    intro = Config.WELCOME_MESSAGE_ENG if lang == "en" else Config.WELCOME_MESSAGE_RUS

    desc = f"{greeting}\n\n{intro}\n\n{body}"

    embed = discord.Embed(
        title=t(lang, "onboarding_title"),
        description=desc,
        color=discord.Color.gold(),
    )
    return embed


def _build_game_roles_embed(lang: str) -> discord.Embed:
    return discord.Embed(
        title=t(lang, "game_roles_title"),
        description=t(lang, "game_roles_body"),
        color=discord.Color.dark_gold(),
    )


# --------- VIEW С ТРЕМЯ КНОПКАМИ ПОСЛЕ ВЫБОРА ЯЗЫКА ---------


class OnboardingMainView(discord.ui.View):
    """
    Главное меню онбординга в ЛС:
    - Игровые роли
    - Стать рекрутом
    - Привязать Steam ID
    """

    def __init__(self, bot: commands.Bot, guild_id: int, lang: str):
        super().__init__(timeout=3600)
        self.bot = bot
        self.guild_id = guild_id
        self.lang = lang

        self.add_item(ChooseGamesButton())
        self.add_item(RegisterRecruitButton())
        self.add_item(LinkSteamButton(lang))


class ChooseGamesButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label=t("en", "btn_games"),  # реальный язык возьмём из view
            style=discord.ButtonStyle.secondary,
            custom_id="choose_games",
        )

    async def callback(self, interaction: discord.Interaction):
        view: OnboardingMainView = self.view  # type: ignore
        lang = view.lang

        guild = interaction.client.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                t(lang, "guild_not_found"),
                ephemeral=True,
            )
            return

        # На всякий пожарный достаём участника
        member = guild.get_member(interaction.user.id)
        if member is None:
            try:
                member = await guild.fetch_member(interaction.user.id)
            except discord.DiscordException:
                await interaction.response.send_message(
                    t(lang, "not_in_guild"),
                    ephemeral=True,
                )
                return

        if not _get_game_role_definitions():
            await interaction.response.send_message(
                t(lang, "no_game_roles"),
                ephemeral=True,
            )
            return

        embed = _build_game_roles_embed(lang)
        roles_view = GameRolesView(bot=view.bot, guild_id=view.guild_id, lang=lang)

        await interaction.response.send_message(
            embed=embed,
            view=roles_view,
            ephemeral=True,
        )


class GameRolesView(discord.ui.View):
    """View с кнопками по играм, которые просто тумблерят роли."""

    def __init__(self, bot: commands.Bot, guild_id: int, lang: str):
        super().__init__(timeout=300)
        self.bot = bot
        self.guild_id = guild_id
        self.lang = lang

        for role_cfg in _get_game_role_definitions():
            self.add_item(GameRoleToggleButton(role_cfg, lang))


class GameRoleToggleButton(discord.ui.Button):
    def __init__(self, role_cfg: dict, lang: str):
        self.role_id: int = int(role_cfg.get("id", 0))

        label = (
            role_cfg.get("label_ru")
            if lang == "ru"
            else role_cfg.get("label_en")
        ) or role_cfg.get("label") or "Role"

        emoji = role_cfg.get("emoji")

        super().__init__(
            label=label,
            emoji=emoji,
            style=discord.ButtonStyle.primary,
            custom_id=f"game_role_{self.role_id}",
        )

    async def callback(self, interaction: discord.Interaction):
        view: GameRolesView = self.view  # type: ignore
        lang = view.lang

        guild = interaction.client.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                t(lang, "guild_not_found"),
                ephemeral=True,
            )
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            try:
                member = await guild.fetch_member(interaction.user.id)
            except discord.DiscordException:
                await interaction.response.send_message(
                    t(lang, "not_in_guild"),
                    ephemeral=True,
                )
                return

        role = guild.get_role(self.role_id)
        if role is None:
            await interaction.response.send_message(
                t(lang, "game_role_not_found"),
                ephemeral=True,
            )
            return

        try:
            if role in member.roles:
                await member.remove_roles(
                    role, reason="Game role toggle via onboarding DM"
                )
                text = t(lang, "game_role_removed").format(role=role.name)
            else:
                await member.add_roles(
                    role, reason="Game role toggle via onboarding DM"
                )
                text = t(lang, "game_role_added").format(role=role.name)

            await interaction.response.send_message(text, ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                t(lang, "no_permission_manage_roles"),
                ephemeral=True,
            )


# ------------ REGISTER RECRUIT BUTTON (DM) ------------


class RegisterRecruitButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label=t("en", "btn_recruit"),
            style=discord.ButtonStyle.success,
            custom_id="register_recruit",
        )

    async def callback(self, interaction: discord.Interaction):
        view: OnboardingMainView = self.view  # type: ignore

        guild = interaction.client.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                t(view.lang, "guild_not_found"),
                ephemeral=True,
            )
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            await interaction.response.send_message(
                t(view.lang, "not_in_guild"),
                ephemeral=True,
            )
            return

        # актуализируем профиль и читаем язык
        user = get_or_create_user_from_member(member)
        lang = user.language or view.lang or "en"

        # проверяем статус рекрута по БД
        status = (user.recruit_status or "pending").lower()
        if status in ("ready", "done"):
            await interaction.response.send_message(
                t(lang, "recruit_already_applied"),
                ephemeral=True,
            )
            return

        # если уже есть каналы рекрута – не плодим дубликаты
        if user.recruit_text_channel_id or user.recruit_voice_channel_id:
            await interaction.response.send_message(
                t(lang, "recruit_already_applied"),
                ephemeral=True,
            )
            return

        # проверка Steam ID
        if not user.steam_id:
            # даём текст + кнопку для модалки
            await interaction.response.send_message(
                t(lang, "steam_link"),
                view=SteamLinkView(lang),
                ephemeral=True,
            )
            return

        recruit_id = RECRUIT_ROLE_ID
        if not recruit_id:
            await interaction.response.send_message(
                t(lang, "recruit_role_not_configured"),
                ephemeral=True,
            )
            return

        recruit_role = guild.get_role(recruit_id)
        if not recruit_role:
            await interaction.response.send_message(
                t(lang, "recruit_role_not_found"),
                ephemeral=True,
            )
            return

        if recruit_role in member.roles:
            await interaction.response.send_message(
                t(lang, "recruit_already_has_role"),
                ephemeral=True,
            )
            return

        try:
            await member.add_roles(recruit_role, reason="Recruit registration via DM")
        except discord.Forbidden:
            await interaction.response.send_message(
                t(lang, "recruit_cannot_grant_role"),
                ephemeral=True,
            )
            return

        # статус в БД
        set_recruit_status(member.id, "ready")

        # создаём личные каналы
        try:
            text_ch, voice_ch, is_new = await ensure_recruit_channels(guild, member)
        except Exception as e:
            print(f"[recruit channels ERROR] {type(e).__name__}: {e}", file=sys.stderr)
            await interaction.response.send_message(
                "Recruit role assigned, but interview channels could not be created. "
                "Please contact staff.",
                ephemeral=True,
            )
            return

        if not is_new:
            await interaction.response.send_message(
                (
                    f'Recruit role "{recruit_role.name}" assigned!\n'
                    f'Your application status: **READY**.\n\n'
                    f'Your interview channels already exist:\n'
                    f'- Text: {text_ch.mention}\n'
                    f'- Voice: {voice_ch.mention}'
                ),
                ephemeral=True,
            )
            return

        # обновим user
        user = get_or_create_user_from_member(member)
        lang = user.language or lang

        # Стим-ссылка
        if getattr(user, "steam_url", None):
            steam_url = user.steam_url
        elif user.steam_id:
            steam_url = f"https://steamcommunity.com/profiles/{user.steam_id}"
        else:
            steam_url = None

        recruit_code = get_recruit_code(user)

        embed = discord.Embed(
            title=t(lang, "recruit_embed_title").format(name=member.display_name),
            color=discord.Color.gold(),
        )

        embed.add_field(
            name="Recruit code",
            value=recruit_code,
            inline=False,
        )

        embed.add_field(
            name="Discord",
            value=(
                f"{member.mention}\n"
                f"Display name: **{member.display_name}**\n"
                f"Username: `{member.name}`\n"
                f"ID: `{member.id}`"
            ),
            inline=False,
        )

        if steam_url:
            embed.add_field(
                name="Steam",
                value=f"ID: `{user.steam_id}`\n[Open profile]({steam_url})",
                inline=False,
            )
        else:
            embed.add_field(
                name="Steam",
                value="Not linked",
                inline=False,
            )

        lang_name = {"ru": "Русский", "en": "English"}.get(user.language, "English")

        embed.add_field(
            name="Language",
            value=lang_name,
            inline=True,
        )

        embed.add_field(
            name="Status",
            value=t(lang, "recruit_embed_status_ready"),
            inline=True,
        )

        embed.set_footer(text="Use this channel to schedule and run the interview.")

        ping_role = member.guild.get_role(getattr(Config, "RECRUITER_ROLE_ID", 0))
        content = f"{member.mention} {ping_role.mention}" if ping_role else member.mention

        mod_view = RecruitModerationView(
            guild_id=guild.id,
            recruit_id=member.id,
            text_channel_id=text_ch.id,
            voice_channel_id=voice_ch.id,
        )

        msg = await text_ch.send(
            content=content,
            embed=embed,
            view=mod_view,
            allowed_mentions=discord.AllowedMentions(users=True, roles=True),
        )

        # чтобы потом можно было корректно задизейблить кнопки
        mod_view.message_id = msg.id

        # ответ рекруту в DM-контексте
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


# ------------ ВЫБОР ЯЗЫКА ------------


class LanguageSelectView(discord.ui.View):
    """Первый шаг: выбор языка."""

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
        view: LanguageSelectView = self.view  # type: ignore

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

        await send_main_menu_dm(bot=view.bot, member=member, lang=self.code)


# ------------ DM HELPERS ------------


async def send_main_menu_dm(bot: commands.Bot, member: discord.Member, lang: str):
    """Отправить главное onboarding-сообщение с тремя кнопками."""
    embed = _build_onboarding_embed(member, lang)
    view = OnboardingMainView(bot=bot, guild_id=member.guild.id, lang=lang)
    await member.send(embed=embed, view=view)


async def send_onboarding_dm(bot: commands.Bot, member: discord.Member) -> bool:
    """Первое ЛС: выбор языка."""
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
    """Если ЛС закрыты — пишем в fallback-канал."""
    chan_id = getattr(Config, "FALLBACK_CHANNEL_ID", 0)
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
