import discord
from discord.ext import commands
from dms.localization import t
from dms.onboarding_flow import send_onboarding_dm
from utils.lang import get_lang_for_member, get_lang_for_user


class Onboarding(commands.Cog):
    """Onboarding & recruit-related commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _get_lang(self, member: discord.Member | discord.User) -> str:
        """Return the preferred language for the member or default to English."""
        if isinstance(member, discord.Member):
            return get_lang_for_member(member)
        if isinstance(member, discord.abc.User):
            return get_lang_for_user(member)
        return "en"

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
        lang = self._get_lang(ctx.author)
        if ctx.guild is None:
            await ctx.reply(
                t(lang, "onboarding_guild_only"),
                mention_author=False,
            )
            return

        member: discord.Member = ctx.author  # type: ignore[assignment]
        sent = await send_onboarding_dm(self.bot, member)

        if sent:
            await ctx.reply(
                t(lang, "onboarding_dm_sent_self"),
                mention_author=False,
            )
        else:
            await ctx.reply(
                t(lang, "onboarding_dm_failed_self"),
                mention_author=False,
            )

    @commands.command(
        name="onboarding_for",
        usage="<@user>",
        help="Send onboarding DM to a specific member.",
        extras={"admin_only": True}  # Visible in help only for admins
    )
    @commands.has_permissions(manage_guild=True)  # Require manage_guild permission
    async def onboarding_for(self, ctx: commands.Context, member: discord.Member):
        """
        Send onboarding DM to a specific member.
        Example: !onboarding_for @Nickname
        """
        lang = self._get_lang(ctx.author)
        if ctx.guild is None:
            await ctx.reply(
                t(lang, "onboarding_guild_only"),
                mention_author=False,
            )
            return

        sent = await send_onboarding_dm(self.bot, member)

        if sent:
            await ctx.reply(
                t(lang, "onboarding_dm_sent_other").format(member=member.mention),
                mention_author=False,
            )
        else:
            await ctx.reply(
                t(lang, "onboarding_dm_failed_other").format(member=member.mention),
                mention_author=False,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Onboarding(bot))
# ------------ END OF FILE ------------
