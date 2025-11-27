"""General commands cog.
Contains general utility and information commands.
"""

import time
import platform
import discord
from discord.ext import commands

from dms.localization import t
from utils.lang import get_lang_for_member, get_lang_for_user


class General(commands.Cog):
    """General utility commands for the bot."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = time.time()

    def _get_lang(self, ctx: commands.Context) -> str:
        """Return the preferred language for the author or default to English."""
        if isinstance(ctx.author, discord.Member):
            return get_lang_for_member(ctx.author)
        if isinstance(ctx.author, discord.abc.User):
            return get_lang_for_user(ctx.author)
        return "en"

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """
        Check the bot's latency.

        Usage: !ping
        """
        lang = self._get_lang(ctx)
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title=t(lang, "ping_title"),
            description=t(lang, "ping_description").format(latency=latency),
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="info", aliases=["botinfo", "about"])
    async def info(self, ctx: commands.Context) -> None:
        """
        Display information about the bot.

        Usage: !info
        """
        lang = self._get_lang(ctx)
        uptime = time.time() - self.start_time
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)

        embed = discord.Embed(
            title=t(lang, "info_title"),
            description=t(lang, "info_description"),
            color=discord.Color.blue(),
        )

        embed.add_field(
            name=t(lang, "info_field_bot"),
            value=f"{self.bot.user.name}#{self.bot.user.discriminator}",
            inline=True,
        )
        embed.add_field(
            name=t(lang, "info_field_servers"),
            value=str(len(self.bot.guilds)),
            inline=True,
        )
        embed.add_field(
            name=t(lang, "info_field_users"),
            value=str(sum(guild.member_count for guild in self.bot.guilds)),
            inline=True,
        )
        embed.add_field(
            name=t(lang, "info_field_uptime"),
            value=t(lang, "info_uptime_value").format(
                hours=hours,
                minutes=minutes,
                seconds=seconds,
            ),
            inline=True,
        )
        embed.add_field(
            name=t(lang, "info_field_python_version"),
            value=platform.python_version(),
            inline=True,
        )
        embed.add_field(
            name=t(lang, "info_field_discordpy_version"),
            value=discord.__version__,
            inline=True,
        )

        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed.set_footer(
            text=t(lang, "requested_by").format(requester=ctx.author),
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )

        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=["server", "guild"])
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context) -> None:
        """
        Display information about the current server.

        Usage: !serverinfo
        """
        lang = self._get_lang(ctx)
        guild = ctx.guild

        embed = discord.Embed(
            title=t(lang, "serverinfo_title").format(name=guild.name),
            color=discord.Color.blue(),
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(
            name=t(lang, "serverinfo_owner"),
            value=guild.owner.mention if guild.owner else t(lang, "unknown_value"),
            inline=True,
        )
        embed.add_field(
            name=t(lang, "serverinfo_members"),
            value=guild.member_count,
            inline=True,
        )
        embed.add_field(
            name=t(lang, "serverinfo_channels"),
            value=t(lang, "serverinfo_channels_value").format(
                text=len(guild.text_channels),
                voice=len(guild.voice_channels),
            ),
            inline=True,
        )
        embed.add_field(
            name=t(lang, "serverinfo_roles"),
            value=len(guild.roles),
            inline=True,
        )
        embed.add_field(
            name=t(lang, "serverinfo_id"),
            value=guild.id,
            inline=True,
        )
        embed.add_field(
            name=t(lang, "serverinfo_created_at"),
            value=(
                guild.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
                if guild.created_at
                else t(lang, "unknown_value")
            ),
            inline=True,
        )

        embed.set_footer(
            text=t(lang, "requested_by").format(requester=ctx.author),
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )

        await ctx.send(embed=embed)

    @commands.command(name="userinfo", aliases=["user", "whois"])
    @commands.guild_only()
    async def userinfo(
        self,
        ctx: commands.Context,
        member: discord.Member | None = None,
    ) -> None:
        """
        Display information about a user.

        Usage: !userinfo [@member]
        Example: !userinfo @John

        If no member is specified, shows info about yourself.
        """
        lang = self._get_lang(ctx)
        member = member or ctx.author

        color = (
            member.color
            if member.color != discord.Color.default()
            else discord.Color.blue()
        )

        embed = discord.Embed(
            title=t(lang, "userinfo_title"),
            color=color,
        )

        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        embed.add_field(
            name=t(lang, "userinfo_name"),
            value=f"{member.name}#{member.discriminator}",
            inline=True,
        )
        embed.add_field(
            name=t(lang, "userinfo_nickname"),
            value=member.nick if member.nick else t(lang, "userinfo_no_nickname"),
            inline=True,
        )
        embed.add_field(
            name=t(lang, "userinfo_id"),
            value=member.id,
            inline=True,
        )
        embed.add_field(
            name=t(lang, "userinfo_status"),
            value=str(member.status).title(),
            inline=True,
        )
        embed.add_field(
            name=t(lang, "userinfo_joined"),
            value=(
                member.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC")
                if member.joined_at
                else t(lang, "unknown_value")
            ),
            inline=True,
        )
        embed.add_field(
            name=t(lang, "userinfo_created"),
            value=member.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
            inline=True,
        )

        roles = [role.mention for role in member.roles[1:]]
        if roles:
            roles_str = ", ".join(roles)
            roles_value = (
                roles_str
                if len(roles_str) <= 1024
                else t(lang, "roles_count_only").format(count=len(roles))
            )
            embed.add_field(
                name=t(lang, "userinfo_roles_title").format(count=len(roles)),
                value=roles_value,
                inline=False,
            )

        embed.set_footer(
            text=t(lang, "requested_by").format(requester=ctx.author),
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )

        await ctx.send(embed=embed)

    @commands.command(name="avatar", aliases=["av", "pfp"])
    async def avatar(
        self,
        ctx: commands.Context,
        member: discord.Member | None = None,
    ) -> None:
        """
        Display a user's avatar.

        Usage: !avatar [@member]
        Example: !avatar @John

        If no member is specified, shows your avatar.
        """
        lang = self._get_lang(ctx)
        member = member or ctx.author

        embed = discord.Embed(
            title=t(lang, "avatar_title").format(name=member.name),
            color=discord.Color.blue(),
        )

        if member.avatar:
            embed.set_image(url=member.avatar.url)
            embed.add_field(
                name=t(lang, "avatar_download_links"),
                value=t(lang, "avatar_download_links_value").format(
                    png=member.avatar.replace(format="png").url,
                    jpg=member.avatar.replace(format="jpg").url,
                    webp=member.avatar.replace(format="webp").url,
                ),
                inline=False,
            )
        else:
            embed.description = t(lang, "avatar_no_custom")

        embed.set_footer(
            text=t(lang, "requested_by").format(requester=ctx.author),
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )

        await ctx.send(embed=embed)

    @commands.command(name="say")
    @commands.has_permissions(administrator=True)
    async def say(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | None = None,
        *,
        text: str,
    ) -> None:
        """
        Send a message to the specified channel or the current channel.

        Examples:
        !say message text
            Sends the text to the current channel.

        !say #channel message text
            Sends the text to the specified channel.

        !say #channel Title | Body --embed
            Sends an embed using title and description split by "|".
        """
        lang = self._get_lang(ctx)
        use_embed = False
        flag = "--embed"

        # Detect optional embed flag at the end of the message text.
        if text.endswith(flag):
            use_embed = True
            text = text[:-len(flag)].strip()

        target_channel = channel or ctx.channel

        if not text:
            await ctx.send(t(lang, "say_nothing_to_send"))
            return

        if use_embed:
            # Parse optional "Title | Body" pattern for embed content.
            title = None
            description = text

            if "|" in text:
                raw_title, raw_body = text.split("|", 1)
                title = raw_title.strip() or None
                description = raw_body.strip() or None

            embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Color.blurple(),
            )
            embed.set_footer(
                text=t(lang, "requested_by").format(requester=ctx.author),
                icon_url=ctx.author.display_avatar.url
                if ctx.author.display_avatar
                else None,
            )
            await target_channel.send(embed=embed)
        else:
            await target_channel.send(text)

        # Ignore message deletion errors when lacking permissions.
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass


async def setup(bot: commands.Bot) -> None:
    """Setup function to add the cog to the bot."""
    await bot.add_cog(General(bot))
