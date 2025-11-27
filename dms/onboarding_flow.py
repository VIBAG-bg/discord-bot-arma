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


# --------- Config helpers ---------


def _get_game_role_definitions():
    """Return configured game role definitions or an empty list."""
    return getattr(Config, "GAME_ROLE_DEFINITIONS", []) or []


def _get_arma_role_definitions():
    """Return configured ARMA role definitions or an empty list."""
    return getattr(Config, "ARMA_ROLE_DEFINITIONS", []) or []


def _build_arma_roles_embed(lang: str) -> discord.Embed:
    return discord.Embed(
        title=t(lang, "arma_roles_title"),
        description=t(lang, "arma_roles_body"),
        color=discord.Color.dark_gold(),
    )



def _build_onboarding_embed(member: discord.Member, lang: str) -> discord.Embed:
    """Build the onboarding embed that greets a user and links to setup actions."""
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


# --------- Views for interactive onboarding in DMs ---------


class OnboardingMainView(discord.ui.View):
    """
    Main onboarding view with entry points to:
    - Choose game roles
    - Register as recruit
    - Link Steam ID
    """

    def __init__(self, bot: commands.Bot, guild_id: int, lang: str):
        super().__init__(timeout=3600)
        self.bot = bot
        self.guild_id = guild_id
        self.lang = lang

        self.add_item(ChooseGamesButton(lang))
        self.add_item(RegisterRecruitButton(lang))
        self.add_item(LinkSteamButton(lang))


class ChooseGamesButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label=t("en", "btn_games"),  # Use English label for a consistent entry point
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

        # Make sure the member exists and can be fetched
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
    """View that lists configured game roles and lets the user toggle them."""

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
        ) or role_cfg.get("label") or t(lang, "role_default_label")

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


class ArmaRolesView(discord.ui.View):
    """View for ARMA operation roles available only to recruits with status 'done'."""

    def __init__(self, bot: commands.Bot, guild_id: int, lang: str):
        super().__init__(timeout=300)
        self.bot = bot
        self.guild_id = guild_id
        self.lang = lang

        for role_cfg in _get_arma_role_definitions():
            self.add_item(ArmaRoleToggleButton(role_cfg, lang))


class ArmaRoleToggleButton(discord.ui.Button):
    def __init__(self, role_cfg: dict, lang: str):
        self.role_id: int = int(role_cfg.get("id", 0))

        label = (
            role_cfg.get("label_ru")
            if lang == "ru"
            else role_cfg.get("label_en")
        ) or role_cfg.get("label") or t(lang, "role_default_label")

        emoji = role_cfg.get("emoji")

        super().__init__(
            label=label,
            emoji=emoji,
            style=discord.ButtonStyle.primary,
            custom_id=f"arma_role_{self.role_id}",
        )

    async def callback(self, interaction: discord.Interaction):
        view: ArmaRolesView = self.view  # type: ignore
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

        from database.service import get_or_create_user_from_member  # Local import to keep context fresh
        user = get_or_create_user_from_member(member)
        status = (user.recruit_status or "pending").lower()

        if status != "done":
            await interaction.response.send_message(
                t(lang, "arma_roles_not_done"),
                ephemeral=True,
            )
            return

        role = guild.get_role(self.role_id)
        if role is None:
            await interaction.response.send_message(
                t(lang, "arma_role_not_found"),
                ephemeral=True,
            )
            return

        try:
            if role in member.roles:
                await member.remove_roles(
                    role,
                    reason="ARMA role toggle via roles panel",
                )
                text = t(lang, "arma_role_removed").format(role=role.name)
            else:
                await member.add_roles(
                    role,
                    reason="ARMA role toggle via roles panel",
                )
                text = t(lang, "arma_role_added").format(role=role.name)

            await interaction.response.send_message(text, ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                t(lang, "no_permission_manage_roles"),
                ephemeral=True,
            )


# ------------ REGISTER RECRUIT BUTTON (DM) ------------


class RegisterRecruitButton(discord.ui.Button):
    def __init__(self, lang: str | None = None):
        super().__init__(
            label=t(lang or "en", "btn_recruit"),
            style=discord.ButtonStyle.success,
            custom_id="register_recruit",
        )
        self.lang = lang or "en"

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

        # Refresh user data to get language preference
        user = get_or_create_user_from_member(member)
        lang = user.language or view.lang or self.lang

        # Prevent duplicate applications when status already set
        status = (user.recruit_status or "pending").lower()
        if status in ("ready", "done"):
            await interaction.response.send_message(
                t(lang, "recruit_already_applied"),
                ephemeral=True,
            )
            return

        # Prevent duplicate channels if they already exist
        if user.recruit_text_channel_id or user.recruit_voice_channel_id:
            await interaction.response.send_message(
                t(lang, "recruit_already_applied"),
                ephemeral=True,
            )
            return

        # Require a linked Steam ID
        if not user.steam_id:
            # Remind to link Steam ID first
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

        # Mark recruit as ready
        set_recruit_status(member.id, "ready")

        # Ensure recruit channels exist
        try:
            text_ch, voice_ch, is_new = await ensure_recruit_channels(guild, member)
        except Exception as e:
            print(f"[recruit channels ERROR] {type(e).__name__}: {e}", file=sys.stderr)
            await interaction.response.send_message(
                t(lang, "recruit_channels_error"),
                ephemeral=True,
            )
            return

        if not is_new:
            await interaction.response.send_message(
                t(lang, "recruit_channels_existing").format(
                    role=recruit_role.name,
                    text=text_ch.mention,
                    voice=voice_ch.mention,
                ),
                ephemeral=True,
            )
            return

        # Reload user to ensure fresh language preference
        user = get_or_create_user_from_member(member)
        lang = user.language or lang

        # Build Steam URL if available
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
            name=t(lang, "recruit_embed_field_code"),
            value=recruit_code,
            inline=False,
        )

        embed.add_field(
            name=t(lang, "recruit_embed_field_discord"),
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
                name=t(lang, "recruit_embed_field_steam"),
                value=f"ID: `{user.steam_id}`\n[Open profile]({steam_url})",
                inline=False,
            )
        else:
            embed.add_field(
                name=t(lang, "recruit_embed_field_steam"),
                value=t(lang, "recruit_embed_steam_not_linked"),
                inline=False,
            )

        lang_name = {
            "ru": t(lang, "language_name_ru"),
            "en": t(lang, "language_name_en"),
        }.get(user.language, t(lang, "language_name_en"))

        embed.add_field(
            name=t(lang, "recruit_embed_field_language"),
            value=lang_name,
            inline=True,
        )

        embed.add_field(
            name=t(lang, "recruit_embed_field_status"),
            value=t(lang, "recruit_embed_status_ready"),
            inline=True,
        )

        embed.set_footer(text=t(lang, "recruit_embed_footer_interview"))

        ping_role = member.guild.get_role(getattr(Config, "RECRUITER_ROLE_ID", 0))
        content = f"{member.mention} {ping_role.mention}" if ping_role else member.mention

        mod_view = RecruitModerationView(
            guild_id=guild.id,
            recruit_id=member.id,
            text_channel_id=text_ch.id,
            voice_channel_id=voice_ch.id,
            recruit_lang=lang,
        )

        msg = await text_ch.send(
            content=content,
            embed=embed,
            view=mod_view,
            allowed_mentions=discord.AllowedMentions(users=True, roles=True),
        )

        # Store message ID to enable moderation callbacks later
        mod_view.message_id = msg.id

        # Confirm to the recruit via DM interaction
        await interaction.response.send_message(
            t(lang, "recruit_channels_created").format(
                role=recruit_role.name,
                text=text_ch.mention,
                voice=voice_ch.mention,
            ),
            ephemeral=True,
        )


# ------------ Language choice ------------


class LanguageSelectView(discord.ui.View):
    """Language selector view shown in onboarding DMs."""

    def __init__(self, bot_client: commands.Bot, guild_id: int):
        super().__init__(timeout=900)
        self.bot = bot_client
        self.guild_id = guild_id
        self.add_item(LanguageButton("en", t("en", "language_name_en")))
        self.add_item(LanguageButton("ru", t("ru", "language_name_ru")))
        self.add_item(LanguageButton("uk", t("uk", "language_name_uk")))


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

        try:
            await send_main_menu_dm(bot=view.bot, member=member, lang=self.code)
        except discord.Forbidden:
            try:
                await interaction.followup.send(
                    t(self.code, "onboarding_dm_failed_self"),
                    ephemeral=True,
                )
            except discord.InteractionResponded:
                pass
        except Exception as e:
            print(f"[LanguageSelect ERROR] {type(e).__name__}: {e}", file=sys.stderr)


# ------------ DM HELPERS ------------


async def send_main_menu_dm(bot: commands.Bot, member: discord.Member, lang: str):
    """Send the main onboarding menu with action buttons."""
    embed = _build_onboarding_embed(member, lang)
    view = OnboardingMainView(bot=bot, guild_id=member.guild.id, lang=lang)
    await member.send(embed=embed, view=view)


async def send_onboarding_dm(bot: commands.Bot, member: discord.Member) -> bool:
    """Send the onboarding language selection DM to a member."""
    if member.bot or member.guild is None:
        return True

    try:
        get_or_create_user(member.id)
        update_discord_profile(member)

        text = f"{t('en', 'choose_language')} / {t('ru', 'choose_language')} / {t('uk', 'choose_language')}"

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
    """Notify in fallback channel when the user's DMs are closed."""
    chan_id = getattr(Config, "FALLBACK_CHANNEL_ID", 0)
    if not chan_id:
        return

    user = get_or_create_user(member.id)
    lang = user.language or getattr(Config, "DEFAULT_LANG", "en")

    channel = bot.get_channel(chan_id)
    if channel is None:
        try:
            channel = await bot.fetch_channel(chan_id)
        except Exception as e:
            print(f"Cannot fetch fallback channel: {e}", file=sys.stderr)
            return

    await channel.send(
        t(lang, "notify_dm_disabled").format(
            member=member.mention,
            command="!onboarding",
        )
    )
