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
    """Handle onboarding-related join events and notifications."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --------- Event listeners ---------

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Handle member joins and initiate onboarding."""
        if member.bot:
            return

        # Log the join so any issues are easier to debug
        print(f"[on_member_join] New member: {member} ({member.id})", file=sys.stderr)

        # Create or update the user record in the database
        try:
            get_or_create_user_from_member(member)
            update_discord_profile(member)
        except Exception as e:
            print(f"[on_member_join DB ERROR] {type(e).__name__}: {e}", file=sys.stderr)

        # Send onboarding DM to the member
        ok = await send_onboarding_dm(self.bot, member)
        if not ok:
            # If DMs are closed, notify in the fallback channel
            try:
                await notify_dm_disabled(self.bot, member)
            except Exception as e:
                print(f"[notify_dm_disabled ERROR] {type(e).__name__}: {e}", file=sys.stderr)


async def setup(bot: commands.Bot):
    await bot.add_cog(OnboardingEvents(bot))
