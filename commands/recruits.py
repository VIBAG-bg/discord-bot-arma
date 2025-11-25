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

STATUSES = ["pending", "ready", "done", "rejected"]


class RecruitCommands(commands.Cog):
    """Команды для работы с рекрутами и синхронизации пользователей."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ========= !recruit =========

    @commands.command(name="recruit")
    async def recruit(self, ctx: commands.Context, member: discord.Member | None = None):
        """
        Показать подробную информацию о рекруте.
        Без аргументов — про тебя, с аргументом — про указанного пользователя.

        Примеры:
          !recruit
          !recruit @User
        """
        target = member or ctx.author

        # На случай если это не Member (хотя в гильдии обычно Member)
        if not isinstance(target, discord.Member):
            guild = ctx.guild
            if guild is not None:
                try:
                    target = await guild.fetch_member(target.id)  # type: ignore
                except discord.DiscordException:
                    await ctx.send("User is not a member of this guild.")
                    return

        user = get_or_create_user_from_member(target)
        lang = user.language or "en"
        status = (user.recruit_status or "pending").lower()

        # Стим-ссылка
        if user.steam_url:
            steam_url = user.steam_url
        elif user.steam_id:
            steam_url = f"https://steamcommunity.com/profiles/{user.steam_id}"
        else:
            steam_url = None

        # Каналы
        text_mention = (
            f"<#{user.recruit_text_channel_id}>"
            if user.recruit_text_channel_id
            else "—"
        )
        voice_mention = (
            f"<#{user.recruit_voice_channel_id}>"
            if user.recruit_voice_channel_id
            else "—"
        )

        recruit_code = get_recruit_code(user)

        embed = discord.Embed(
            title="Recruit info / Информация о рекруте",
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
                f"{target.mention}\n"
                f"Display name: **{target.display_name}**\n"
                f"Username: `{target.name}`\n"
                f"ID: `{target.id}`"
            ),
            inline=False,
        )

        lang_name = {"ru": "Русский", "en": "English"}.get(user.language, "English")

        embed.add_field(name="Status", value=status.upper(), inline=True)
        embed.add_field(name="Language", value=lang_name, inline=True)

        if steam_url:
            embed.add_field(
                name="Steam",
                value=f"ID: `{user.steam_id}`\n[Open profile]({steam_url})",
                inline=False,
            )
        else:
            embed.add_field(
                name="Steam",
                value="Not linked / Не привязан",
                inline=False,
            )

        embed.add_field(
            name="Text channel",
            value=text_mention,
            inline=True,
        )
        embed.add_field(
            name="Voice channel",
            value=voice_mention,
            inline=True,
        )

        await ctx.send(embed=embed)

    # ========= !recruits =========

    @commands.command(name="recruits")
    @commands.has_permissions(administrator=True)
    async def recruits(self, ctx: commands.Context, status: str | None = None):
        """
        Краткий обзор рекрутов.

        Без аргумента — сводка по всем статусам.
        С аргументом (pending/ready/done/rejected) — только этот статус.

        Примеры:
          !recruits
          !recruits ready
        """
        if status:
            status = status.lower()
            if status not in STATUSES:
                await ctx.send("Unknown status. Use: pending / ready / done / rejected.")
                return

            users = get_recruits_by_status(status)
            if not users:
                await ctx.send(f"No recruits with status **{status}**.")
                return

            lines: list[str] = []
            for u in users:
                line = f"- <@{u.discord_id}> (ID `{u.discord_id}`)"
                if u.steam_id:
                    line += f" | Steam `{u.steam_id}`"
                lines.append(line)

            embed = discord.Embed(
                title=f"Recruits with status {status.upper()}",
                description="\n".join(lines),
                color=discord.Color.blurple(),
            )
            await ctx.send(embed=embed)
            return

        # Без статуса — сводка по всем
        embed = discord.Embed(
            title="Recruits overview",
            color=discord.Color.blurple(),
        )

        for st in STATUSES:
            users = get_recruits_by_status(st)
            if not users:
                value = "_none_"
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
        Обновить одну запись пользователя в БД из текущих данных Discord.
        Если пользователя нет — будет создан.

        Примеры:
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
                    await ctx.send("User is not a member of this guild.")
                    return

        user = get_or_create_user_from_member(target)

        await ctx.send(
            f"User `{target}` synced.\n"
            f"discord_id={user.discord_id}, username=`{user.username}`, "
            f"display_name=`{user.display_name}`, is_admin={user.is_admin}"
        )

    # ========= !user_updates =========

    @commands.command(name="user_updates")
    @commands.has_permissions(administrator=True)
    async def user_updates(self, ctx: commands.Context):
        """
        Массовый апдейт всех пользователей сервера в БД.
        Проходит по всем участникам гильдии и синхронизирует профиль.
        """
        guild = ctx.guild
        if guild is None:
            await ctx.send("This command can only be used in a guild.")
            return

        updated = 0
        for member in guild.members:
            if member.bot:
                continue
            get_or_create_user_from_member(member)
            updated += 1

        await ctx.send(f"Updated {updated} users from guild `{guild.name}`.")


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitCommands(bot))
