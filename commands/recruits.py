# cogs/recruits.py

import discord
from discord.ext import commands

from config import Config
from database.service import (
    get_recruits_all,
    get_recruits_by_status,
    get_user_by_discord_id,
    get_user_by_username,
    get_or_create_user_from_member,
)

STATUSES = ["pending", "ready", "done", "rejected"]


class RecruitCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --- общий чек доступа для всего кога ---

    @staticmethod
    def _is_recruit_mod(member: discord.Member) -> bool:
        # админы сервера
        if member.guild_permissions.administrator or member.guild_permissions.manage_guild:
            return True

        # роли рекрутеров
        recruiter_ids = set(getattr(Config, "RECRUITER_ROLE_IDS", []))
        if getattr(Config, "RECRUITER_ROLE_ID", 0):
            recruiter_ids.add(Config.RECRUITER_ROLE_ID)

        if any(r.id in recruiter_ids for r in member.roles):
            return True

        # is_admin в БД
        db_user = get_or_create_user_from_member(member)
        return bool(getattr(db_user, "is_admin", False))

    async def cog_check(self, ctx: commands.Context) -> bool:
        # все команды этого кога только для рекрутеров / модов / админов
        if not isinstance(ctx.author, discord.Member):
            return False
        return self._is_recruit_mod(ctx.author)

    # ---------- !recruits ----------

    @commands.command(name="recruits")
    @commands.guild_only()
    async def list_recruits(self, ctx: commands.Context):
        """
        Показать всех рекрутов по статусам.
        """
        guild = ctx.guild
        if guild is None:
            return

        embed = discord.Embed(
            title="Recruits overview",
            color=discord.Color.blurple(),
        )

        # по каждому статусу отдельное поле
        for status in STATUSES:
            users = get_recruits_by_status(status)
            if not users:
                value = "_none_"
            else:
                lines: list[str] = []
                for u in users[:30]:  # вдруг их будет много
                    member = guild.get_member(u.discord_id)
                    mention = member.mention if member else f"`{u.discord_id}`"
                    code = getattr(u, "recruit_code", None) or ""
                    if code:
                        lines.append(f"- {mention} (`{code}`)")
                    else:
                        lines.append(f"- {mention}")
                if len(users) > 30:
                    lines.append(f"... и ещё {len(users) - 30} записей")
                value = "\n".join(lines)

            embed.add_field(
                name=status.upper(),
                value=value,
                inline=False,
            )

        embed.set_footer(text="Statuses: pending / ready / done / rejected")

        await ctx.send(embed=embed)

    # ---------- !recruit @user ----------

    @commands.command(name="recruit")
    @commands.guild_only()
    async def recruit_info(self, ctx: commands.Context, member: discord.Member):
        """
        Показать инфу по одному человеку (через @mention):
        статус рекрута, Steam, текст/войс-каналы.
        """
        guild = ctx.guild
        if guild is None:
            return

        # 1. Пытаемся найти по discord_id (правильный путь)
        user = get_user_by_discord_id(member.id)

        # 2. Если вдруг нет, пробуем по username (как ты просил)
        if user is None:
            user = get_user_by_username(member.name)

        if user is None or not user.recruit_status:
            await ctx.send(
                f"{member.mention} не найден в базе как рекрут.",
                allowed_mentions=discord.AllowedMentions(users=False),
            )
            return

        status = (user.recruit_status or "pending").lower()
        lang = user.language or "en"

        # --- Steam ---
        if getattr(user, "steam_url", None):
            steam_url = user.steam_url
        elif getattr(user, "steam_id", None):
            steam_url = f"https://steamcommunity.com/profiles/{user.steam_id}"
        else:
            steam_url = None

        if getattr(user, "steam_id", None):
            if steam_url:
                steam_value = f"ID: `{user.steam_id}`\n[Open profile]({steam_url})"
            else:
                steam_value = f"ID: `{user.steam_id}`"
        else:
            steam_value = "Not linked"

        # --- каналы ---
        text_ch = guild.get_channel(getattr(user, "recruit_text_channel_id", 0))
        voice_ch = guild.get_channel(getattr(user, "recruit_voice_channel_id", 0))

        text_value = text_ch.mention if isinstance(text_ch, discord.TextChannel) else "Not set"
        voice_value = voice_ch.mention if isinstance(voice_ch, discord.VoiceChannel) else "Not set"

        lang_name = {
            "ru": "Русский",
            "en": "English",
        }.get(lang, lang)

        # --- эмбед ---
        embed = discord.Embed(
            title=f"Recruit info: {member.display_name}",
            color=discord.Color.gold(),
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

        embed.add_field(name="Status", value=status.upper(), inline=True)
        embed.add_field(name="Language", value=lang_name, inline=True)

        embed.add_field(name="Steam", value=steam_value, inline=False)
        embed.add_field(name="Text channel", value=text_value, inline=True)
        embed.add_field(name="Voice channel", value=voice_value, inline=True)

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitCommands(bot))
