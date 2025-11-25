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
from dms.recruit_channels import create_recruit_channels
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
    description="ARMA 3 Community Discord Bot"
)


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

    await bot.change_presence(
        activity=discord.Game(name=f"{Config.PREFIX}help | ARMA 3")
    )


@bot.event
async def on_member_remove(member: discord.Member):
    """Notify when someone leaves the server."""
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"{member.name} has left the server.")


@bot.event
async def on_command_error(ctx, error):
    """Global command error handler."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Bad argument: {error}")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Try again in {error.retry_after:.2f}s")
    else:
        print(f"Error: {error}", file=sys.stderr)
        await ctx.send("An error occurred while executing the command.")


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

    text_ch = None
    voice_ch = None

    if getattr(user, "recruit_text_channel_id", None):
        ch = guild.get_channel(user.recruit_text_channel_id)
        if isinstance(ch, discord.TextChannel):
            text_ch = ch

    if getattr(user, "recruit_voice_channel_id", None):
        ch = guild.get_channel(user.recruit_voice_channel_id)
        if isinstance(ch, discord.VoiceChannel):
            voice_ch = ch

    if text_ch is None or voice_ch is None:
        try:
            text_ch, voice_ch = await create_recruit_channels(guild, after)
        except Exception as e:
            print(
                f"[Recruit auto ERROR] Cannot create channels for {after}: {type(e).__name__}: {e}",
                file=sys.stderr,
            )
            return

    status = (user.recruit_status or "").lower()
    if status not in ("done", "rejected"):
        set_recruit_status(after.id, "ready")

    if not getattr(user, "steam_id", None):
        msg_en = (
            "You have been granted the **Recruit** role by staff.\n\n"
            "To complete your registration, please link your SteamID64.\n"
            "Press the button below and fill in the form."
        )
        msg_ru = (
            "Тебе выдали роль **Recruit**.\n\n"
            "Чтобы завершить регистрацию, привяжи свой SteamID64.\n"
            "Нажми на кнопку ниже и заполни форму."
        )
        text = msg_en if lang == "en" else msg_ru

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
