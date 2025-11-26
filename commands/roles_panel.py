import discord
from discord.ext import commands

from config import Config
from dms.localization import t
from dms.onboarding_flow import (
    GameRolesView,
    ArmaRolesView,
    _build_game_roles_embed,
    _build_arma_roles_embed,
    RegisterRecruitButton,
)
from database.service import get_or_create_user_from_member


def _format_game_roles_short(lang: str) -> str:
    """Format a short list of game roles with mentions and descriptions."""
    defs = getattr(Config, "GAME_ROLE_DEFINITIONS", []) or []
    if not defs:
        return t(lang, "no_game_roles")

    lines: list[str] = []
    for cfg in defs:
        role_id = cfg.get("id")
        name = (
            cfg.get("label_ru")
            if lang == "ru"
            else cfg.get("label_en")
        ) or cfg.get("label") or t(lang, "role_default_label")

        desc_key = "description_ru" if lang == "ru" else "description_en"
        desc = cfg.get(desc_key) or ""

        mention = f"<@&{int(role_id)}>" if role_id else name
        if desc:
            lines.append(t(lang, "role_with_description").format(mention=mention, desc=desc))
        else:
            lines.append(mention)

    return "\n".join(lines)


def _format_arma_roles_short(lang: str) -> str:
    """Format a short list of ARMA operation roles with mentions and descriptions."""
    defs = getattr(Config, "ARMA_ROLE_DEFINITIONS", []) or []
    if not defs:
        return t(lang, "no_arma_roles")

    lines: list[str] = []
    for cfg in defs:
        role_id = cfg.get("id")
        name = (
            cfg.get("label_ru")
            if lang == "ru"
            else cfg.get("label_en")
        ) or cfg.get("label") or t(lang, "role_default_label")

        desc_key = "description_ru" if lang == "ru" else "description_en"
        desc = cfg.get(desc_key) or ""

        mention = f"<@&{int(role_id)}>" if role_id else name
        if desc:
            lines.append(t(lang, "role_with_description").format(mention=mention, desc=desc))
        else:
            lines.append(mention)

    return "\n".join(lines)


class PanelGamesButton(discord.ui.Button):
    """Button to open the game roles menu in the roles panel."""

    def __init__(self):
        super().__init__(
            label=t("ru", "btn_games_panel"),  # Keep Russian label for panel entry point
            style=discord.ButtonStyle.primary,
            custom_id="panel_choose_games",
        )

    async def callback(self, interaction: discord.Interaction):
        view: ServerRolesPanelView = self.view  # type: ignore
        lang = view.lang

        guild = interaction.client.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                t(lang, "guild_not_found"),
                ephemeral=True,
            )
            return

        if not getattr(Config, "GAME_ROLE_DEFINITIONS", []):
            await interaction.response.send_message(
                t(lang, "no_game_roles"),
                ephemeral=True,
            )
            return

        embed = _build_game_roles_embed(lang)
        roles_view = GameRolesView(
            bot=view.bot,
            guild_id=view.guild_id,
            lang=lang,
        )

        await interaction.response.send_message(
            embed=embed,
            view=roles_view,
            ephemeral=True,
        )


class PanelArmaButton(discord.ui.Button):
    """Button to open the ARMA roles menu in the roles panel."""

    def __init__(self):
        super().__init__(
            label=t("ru", "btn_arma_panel"),
            style=discord.ButtonStyle.secondary,
            custom_id="panel_choose_arma",
        )

    async def callback(self, interaction: discord.Interaction):
        view: ServerRolesPanelView = self.view  # type: ignore
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

        if not getattr(Config, "ARMA_ROLE_DEFINITIONS", []):
            await interaction.response.send_message(
                t(lang, "no_arma_roles"),
                ephemeral=True,
            )
            return

        user = get_or_create_user_from_member(member)
        status = (user.recruit_status or "pending").lower()

        if status != "done":
            await interaction.response.send_message(
                t(lang, "arma_roles_not_done"),
                ephemeral=True,
            )
            return

        embed = _build_arma_roles_embed(lang)
        arma_view = ArmaRolesView(
            bot=view.bot,
            guild_id=view.guild_id,
            lang=lang,
        )

        await interaction.response.send_message(
            embed=embed,
            view=arma_view,
            ephemeral=True,
        )


class ServerRolesPanelView(discord.ui.View):
    """
    Persistent roles panel view with:
    - game roles menu
    - ARMA roles menu
    - recruit registration
    """

    def __init__(self, bot: commands.Bot, guild_id: int, lang: str):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild_id = guild_id
        self.lang = lang

        self.add_item(PanelGamesButton())
        self.add_item(PanelArmaButton())

        # Clone register button so it can display in the server panel as well
        recruit_btn = RegisterRecruitButton()
        recruit_btn.label = t(lang, "btn_recruit")
        self.add_item(recruit_btn)


class RolesPanel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="role_panel", aliases=["post_roles"])
    @commands.has_permissions(administrator=True)
    async def role_panel(self, ctx: commands.Context):
        """
        Post the roles panel with buttons for:
        - game roles
        - ARMA operation specializations (only if recruit_status='done')
        - register as recruit
        """

        lang = getattr(Config, "DEFAULT_LANG", "ru")

        has_games = bool(getattr(Config, "GAME_ROLE_DEFINITIONS", []) or [])
        has_arma = bool(getattr(Config, "ARMA_ROLE_DEFINITIONS", []) or [])

        if not has_games and not has_arma:
            await ctx.send(t(lang, "no_roles_configured"))
            return

        embed = discord.Embed(
            title=t(lang, "role_panel_title"),
            description=t(lang, "role_panel_body"),
            color=discord.Color.dark_gold(),
        )

        if has_games:
            embed.add_field(
                name=t(lang, "role_panel_games_header"),
                value=_format_game_roles_short(lang),
                inline=False,
            )

        if has_arma:
            embed.add_field(
                name=t(lang, "role_panel_arma_header"),
                value=_format_arma_roles_short(lang),
                inline=False,
            )

        view = ServerRolesPanelView(
            bot=self.bot,
            guild_id=ctx.guild.id,
            lang=lang,
        )

        msg = await ctx.send(embed=embed, view=view)
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        print(f"[role_panel] Posted roles panel in #{ctx.channel} (message ID: {msg.id})")


async def setup(bot: commands.Bot):
    await bot.add_cog(RolesPanel(bot))
