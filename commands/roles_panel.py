import discord
from discord.ext import commands

from dms.localization import t
from dms.onboarding_flow import GameRolesView, _build_game_roles_embed
from config import Config


class RolesPanel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="post_roles")
    @commands.has_permissions(administrator=True)
    async def post_roles(self, ctx: commands.Context):
        """Постит постоянную панель с выбором игровых ролей."""

        # язык панели берём из конфига или ставим EN
        lang = getattr(Config, "DEFAULT_LANG", "en")

        # если нет ролей — предупреждаем
        if not getattr(Config, "GAME_ROLE_DEFINITIONS", []):
            await ctx.send("GAME_ROLE_DEFINITIONS пуст — нечего постить.")
            return

        embed = _build_game_roles_embed(lang)

        view = GameRolesView(
            bot=self.bot,
            guild_id=ctx.guild.id,
            lang=lang
        )

        await ctx.send(embed=embed, view=view)
        await ctx.message.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(RolesPanel(bot))

    
