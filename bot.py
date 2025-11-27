"""
Main Discord Bot for ARMA 3 Community
A modular Discord bot built with discord.py
"""

import discord
from discord.ext import commands
import asyncio
import sys
from config import Config
from dms.steam_link import SteamLinkView
from dms.recruit_channels import ensure_recruit_channels
from dms.recruit_moderation import send_recruit_moderation_embed
from commands.help import EmbedHelpCommand
from database.db import Base, engine
from database import models
from dms.steam_link import SteamLinkView
from database.service import (
    get_or_create_user_from_member,
    update_discord_profile,
    set_recruit_status,
)
from dms.localization import t
from utils.lang import get_lang_for_member, get_lang_for_user


# Configure bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = False

# Initialize bot
bot = commands.Bot(
    command_prefix=Config.PREFIX,
    intents=intents,
    help_command=EmbedHelpCommand(),
    description=t(getattr(Config, "DEFAULT_LANG", "en"), "bot_description"),
)


def _get_lang_from_ctx(ctx: commands.Context) -> str:
    """Return preferred language for the author or default language."""
    author = getattr(ctx, "author", None)
    if isinstance(author, discord.Member):
        return get_lang_for_member(author)
    if isinstance(author, discord.abc.User):
        return get_lang_for_user(author)
    return getattr(Config, "DEFAULT_LANG", "en")


def _get_lang_from_member(member: discord.Member) -> str:
    """Return preferred language for a member or default language."""
    if isinstance(member, discord.Member):
        return get_lang_for_member(member)
    if isinstance(member, discord.abc.User):
        return get_lang_for_user(member)
    return getattr(Config, "DEFAULT_LANG", "en")


@bot.event
async def on_ready():
    """Event handler when bot is ready."""
    print("Bot is ready!")
    print(f"Logged in as: {bot.user.name} (ID: {bot.user.id})")
    print(f"discord.py version: {discord.__version__}")
    print(f"Connected to {len(bot.guilds)} guild(s)")
    print("------")

    # Register UI View globally (persistent across restarts)
    #bot.add_view(RoleSelectionView(bot_client=bot))

    default_lang = getattr(Config, "DEFAULT_LANG", "en")
    await bot.change_presence(
        activity=discord.Game(
            name=t(default_lang, "presence_help_hint").format(prefix=Config.PREFIX)
        )
    )


@bot.event
async def on_member_remove(member: discord.Member):
    """Notify when someone leaves the server."""
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        lang = _get_lang_from_member(member)
        await channel.send(t(lang, "member_left_server").format(name=member.name))


@bot.event
async def on_command_error(ctx, error):
    """Global command error handler."""
    lang = _get_lang_from_ctx(ctx)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(t(lang, "command_not_found").format(prefix=ctx.clean_prefix))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(t(lang, "missing_permissions"))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(t(lang, "missing_required_argument").format(param=error.param))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(t(lang, "bad_argument").format(error=error))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            t(lang, "command_on_cooldown").format(retry_after=error.retry_after)
        )
    else:
        print(f"Error: {error}", file=sys.stderr)
        await ctx.send(t(lang, "error_generic"))


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.bot or after.bot:
        return

    guild = after.guild
    recruit_role = guild.get_role(Config.RECRUIT_ROLE_ID)
    if not recruit_role:
        return

    had_recruit = recruit_role in before.roles
    has_recruit = recruit_role in after.roles

    if had_recruit or not has_recruit:
        return

    user = get_or_create_user_from_member(after)
    update_discord_profile(after)
    lang = user.language or "en"

    try:
        text_ch, voice_ch, is_new = await ensure_recruit_channels(guild, after)
    except Exception as e:
        print(
            f"[Recruit auto ERROR] Cannot create channels for {after}: {type(e).__name__}: {e}",
            file=sys.stderr,
        )
        return

    user = get_or_create_user_from_member(after)

    if is_new:
    
        user = get_or_create_user_from_member(after)

        status = (user.recruit_status or "").lower()
        if status not in ("done", "rejected"):
            set_recruit_status(after.id, "ready")

        if not getattr(user, "steam_id", None):
            text = t(lang, "recruit_auto_granted")

            try:
                await after.send(text, view=SteamLinkView(lang))
            except discord.Forbidden:
                print(
                    f"[Recruit auto] Cannot DM {after} about SteamID (DM closed).",
                    file=sys.stderr,
                )
            except Exception as e:
                print(
                    f"[Recruit auto DM ERROR] {type(e).__name__}: {e}",
                    file=sys.stderr,
                )

        try:
            await send_recruit_moderation_embed(
                guild=guild,
                member=after,
                text_ch=text_ch,
                voice_ch=voice_ch,
            )
        except Exception as e:
            print(
                f"[Recruit auto EMBED ERROR] {type(e).__name__}: {e}",
                file=sys.stderr,
            )

    else:
        return


async def load_extensions():
    """Load all COG modules."""
    extensions = [
        "commands.moderation",
        "commands.general",
        "commands.onboarding",
        "commands.recruits",
        "commands.roles_panel",
        "events.onboarding_events"

    ]
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"Loaded extension: {ext}")
        except Exception as e:
            print(f"Failed to load extension {ext}: {e}", file=sys.stderr)


async def main():
    """Main function to start the bot."""

    try:
        
        # Validate configuration
        Config.validate()
        
        # Load extensions
        await load_extensions()
        
        # Start the bot
        await bot.start(Config.TOKEN)
    except KeyboardInterrupt:
        print("\nShutting down bot...")
        await bot.close()
    except Exception as e:
        print(f"Error starting bot: {e}", file=sys.stderr)
        sys.exit(1)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped.")
