import discord
from discord.ext import commands
from dms.onboarding import send_onboarding_dm


class Onboarding(commands.Cog):
    """Onboarding & recruit-related commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="onboarding",
        usage="",
        help="Resend onboarding DM to yourself."
    )
    async def onboarding_self(self, ctx: commands.Context):
        """
        Resend onboarding DM to the command author.
        Use in a server text channel.
        """
        if ctx.guild is None:
            await ctx.reply(
                "This command must be used in a server channel, not in DMs.",
                mention_author=False,
            )
            return

        member: discord.Member = ctx.author  # type: ignore[assignment]
        sent = await send_onboarding_dm(self.bot, member)

        if sent:
            await ctx.reply(
                "Onboarding DM has been sent to you.",
                mention_author=False,
            )
        else:
            await ctx.reply(
                "I couldn't send you a DM. Please enable DMs from server members and try again.",
                mention_author=False,
            )


    @commands.command(
        name="onboarding_for",
        usage="<@user>",
        help="Send onboarding DM to a specific member.",
        extras={"admin_only": True}  # ← помечаем как админскую
    )
    @commands.has_permissions(manage_guild=True)  # офицеры/админы
    async def onboarding_for(self, ctx: commands.Context, member: discord.Member):
        """
        Send onboarding DM to a specific member.
        Example: !onboarding_for @Nickname
        """
        if ctx.guild is None:
            await ctx.reply(
                "This command must be used in a server channel, not in DMs.",
                mention_author=False,
            )
            return

        sent = await send_onboarding_dm(self.bot, member)

        if sent:
            await ctx.reply(
                f"Onboarding DM has been sent to {member.mention}.",
                mention_author=False,
            )
        else:
            await ctx.reply(
                f"I couldn't DM {member.mention}. Their DMs may still be disabled.",
                mention_author=False,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Onboarding(bot))
# ------------ END OF FILE ------------