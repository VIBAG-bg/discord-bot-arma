# events/onboarding_events.py

import sys
import discord
from discord.ext import commands

from dms.onboarding_flow import (
    send_onboarding_dm,
    notify_dm_disabled,
)
from database.service import (
    get_or_create_user_from_member,
    update_discord_profile,
)


class OnboardingEvents(commands.Cog):
    """События и команды, связанные с онбордингом."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --------- АВТО-ОНБОРДИНГ ПРИ ВХОДЕ ---------

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Автоматически шлём ЛС с выбором языка, когда кто-то заходит на сервер."""
        if member.bot:
            return

        # Немного логов, чтобы было видно, что событие вообще срабатывает
        print(f"[on_member_join] New member: {member} ({member.id})", file=sys.stderr)

        # Создаём/обновляем юзера в БД
        try:
            get_or_create_user_from_member(member)
            update_discord_profile(member)
        except Exception as e:
            print(f"[on_member_join DB ERROR] {type(e).__name__}: {e}", file=sys.stderr)

        # Пытаемся отправить онбординг в ЛС
        ok = await send_onboarding_dm(self.bot, member)
        if not ok:
            # Если ЛС выключены – уведомляем в fallback-канал
            try:
                await notify_dm_disabled(self.bot, member)
            except Exception as e:
                print(f"[notify_dm_disabled ERROR] {type(e).__name__}: {e}", file=sys.stderr)


async def setup(bot: commands.Bot):
    await bot.add_cog(OnboardingEvents(bot))
