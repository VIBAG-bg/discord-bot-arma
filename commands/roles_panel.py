import discord
from discord.ext import commands

from dms.localization import t
from dms.onboarding_flow import ChooseGamesButton
from config import Config

class GameRolesPanelView(discord.ui.View):
    """
    Серверная панель с одной кнопкой "Choose game".
    Кнопка использует ту же логику, что и в онбординге в ЛС.
    """

    def __init__(self, bot: commands.Bot, guild_id: int, lang: str):
        # timeout=None, чтобы панель не протухала
        super().__init__(timeout=None)
        self.bot = bot
        self.guild_id = guild_id
        self.lang = lang

        # Кнопка уже умеет:
        # - понять lang через self.view.lang
        # - открыть ephemeral embed с GameRolesView
        self.add_item(ChooseGamesButton())



class RolesPanel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="role_panel", aliases=["post_roles"])
    @commands.has_permissions(administrator=True)
    async def role_panel(self, ctx: commands.Context):
        """Постит постоянную панель с выбором игровых ролей через кнопку."""

        lang = getattr(Config, "DEFAULT_LANG", "en")

        # если игровых ролей нет — говорим по-человечески
        if not getattr(Config, "GAME_ROLE_DEFINITIONS", []):
            await ctx.send(t(lang, "no_game_roles"))
            return

        embed = discord.Embed(
            title=t(lang, "game_roles_panel_title"),
            description=t(lang, "game_roles_panel_body"),
            color=discord.Color.dark_gold(),
        )

        view = GameRolesPanelView(
            bot=self.bot,
            guild_id=ctx.guild.id,
            lang=lang,
        )

        await ctx.send(embed=embed, view=view)
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass



async def setup(bot: commands.Bot):
    await bot.add_cog(RolesPanel(bot))

    
