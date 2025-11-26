import discord
from discord.ext import commands

from config import Config
from database.service import (
    get_recruits_all,
    get_recruits_by_status,
    get_user_by_discord_id,
    get_user_by_username,
    get_or_create_user_from_member,
    get_recruit_code,
)
from database.models import User
from dms.localization import t

STATUSES = ["pending", "ready", "done", "rejected"]


class RecruitCommands(commands.Cog):
    """Commands for recruit-related information and synchronization."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ========= !recruit =========

    @commands.command(name="recruit")
    async def recruit(self, ctx: commands.Context, member: discord.Member | None = None):
        """
        Show recruit profile details for yourself or a specified member.

        Examples:
          !recruit
          !recruit @User
        """
        target = member or ctx.author

        # Ensure target is a Member object if a partial user was provided
        if not isinstance(target, discord.Member):
            guild = ctx.guild
            if guild is not None:
                try:
                    target = await guild.fetch_member(target.id)  # type: ignore
                except discord.DiscordException:
                    await ctx.send(t("en", "user_not_in_guild"))
                    return

        user = get_or_create_user_from_member(target)
        lang = user.language or "en"
        status = (user.recruit_status or "pending").lower()

        if user.steam_url:
            steam_url = user.steam_url
        elif user.steam_id:
            steam_url = f"https://steamcommunity.com/profiles/{user.steam_id}"
        else:
            steam_url = None

        text_mention = (
            f"<#{user.recruit_text_channel_id}>"
            if user.recruit_text_channel_id
            else t(lang, "value_unknown")
        )
        voice_mention = (
            f"<#{user.recruit_voice_channel_id}>"
            if user.recruit_voice_channel_id
            else t(lang, "value_unknown")
        )

        recruit_code = get_recruit_code(user)

        embed = discord.Embed(
            title=t(lang, "recruit_info_title"),
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
                f"{target.mention}\n"
                f"Display name: **{target.display_name}**\n"
                f"Username: `{target.name}`\n"
                f"ID: `{target.id}`"
            ),
            inline=False,
        )

        lang_name = {
            "ru": t(lang, "language_name_ru"),
            "en": t(lang, "language_name_en"),
        }.get(user.language, t(lang, "language_name_en"))

        embed.add_field(
            name=t(lang, "recruit_embed_field_status"),
            value=status.upper(),
            inline=True,
        )
        embed.add_field(
            name=t(lang, "recruit_embed_field_language"),
            value=lang_name,
            inline=True,
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
                value=t(lang, "recruit_embed_steam_not_linked_bilingual"),
                inline=False,
            )

        embed.add_field(
            name=t(lang, "recruit_field_text_channel"),
            value=text_mention,
            inline=True,
        )
        embed.add_field(
            name=t(lang, "recruit_field_voice_channel"),
            value=voice_mention,
            inline=True,
        )

        await ctx.send(embed=embed)

    # ========= !recruits =========

    @commands.command(name="recruits")
    @commands.has_permissions(administrator=True)
    async def recruits(self, ctx: commands.Context, status: str | None = None):
        """
        List recruits with an optional status filter.

        Without a status, lists all recruits grouped by status.
        With a status (pending/ready/done/rejected), shows recruits in that status.

        Examples:
          !recruits
          !recruits ready
        """
        default_lang = "en"
        if status:
            status = status.lower()
            if status not in STATUSES:
                await ctx.send(t(default_lang, "recruits_unknown_status"))
                return

            users = get_recruits_by_status(status)
            if not users:
                await ctx.send(
                    t(default_lang, "recruits_none_with_status").format(status=status)
                )
                return

            lines: list[str] = []
            for u in users:
                line = f"- <@{u.discord_id}> (ID `{u.discord_id}`)"
                if u.steam_id:
                    line += f" | Steam `{u.steam_id}`"
                lines.append(line)

            embed = discord.Embed(
                title=t(default_lang, "recruits_with_status_title").format(
                    status=status.upper()
                ),
                description="\n".join(lines),
                color=discord.Color.blurple(),
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title=t(default_lang, "recruits_overview_title"),
            color=discord.Color.blurple(),
        )

        for st in STATUSES:
            users = get_recruits_by_status(st)
            if not users:
                value = t(default_lang, "recruits_overview_none")
            else:
                value_lines = [f"<@{u.discord_id}>" for u in users]
                value = "\n".join(value_lines)

            embed.add_field(
                name=st.upper(),
                value=value,
                inline=False,
            )

        await ctx.send(embed=embed)

    # ========= !user_update =========

    @commands.command(name="user_update")
    @commands.has_permissions(administrator=True)
    async def user_update(self, ctx: commands.Context, member: discord.Member | None = None):
        """
        Synchronize a user's profile fields with Discord data.

        Examples:
          !user_update
          !user_update @User
        """
        target = member or ctx.author

        if not isinstance(target, discord.Member):
            guild = ctx.guild
            if guild is not None:
                try:
                    target = await guild.fetch_member(target.id)  # type: ignore
                except discord.DiscordException:
                    await ctx.send(t("en", "user_not_in_guild"))
                    return

        user = get_or_create_user_from_member(target)

        await ctx.send(
            t("en", "user_synced").format(
                target=target,
                discord_id=user.discord_id,
                username=user.username,
                display_name=user.display_name,
                is_admin=user.is_admin,
            )
        )

    # ========= !user_updates =========

    @commands.command(name="user_updates")
    @commands.has_permissions(administrator=True)
    async def user_updates(self, ctx: commands.Context):
        """
        Bulk refresh user profiles for the current guild.

        Updates every non-bot member so stored data matches Discord state.
        """
        guild = ctx.guild
        if guild is None:
            await ctx.send(t("en", "command_guild_only"))
            return

        updated = 0
        for member in guild.members:
            if member.bot:
                continue
            get_or_create_user_from_member(member)
            updated += 1

        await ctx.send(t("en", "user_updates_done").format(updated=updated, guild=guild.name))


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitCommands(bot))
