"""
Main Discord Bot for ARMA 3 Community
A modular Discord bot built with discord.py
"""

import discord
from discord.ext import commands
import asyncio
import sys
from config import Config
from dms.onboarding import RoleSelectionView, send_onboarding_dm, notify_dm_disabled
from commands.help import EmbedHelpCommand
from database.db import Base, engine
from database import models
from database.service import get_or_create_user


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
async def on_member_join(member: discord.Member):
    """Send DM onboarding. If DM is blocked → notify fallback channel + create user in DB."""
    get_or_create_user(member.id)
    sent = await send_onboarding_dm(bot, member)
    if not sent:
        await notify_dm_disabled(bot, member)


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


async def load_extensions():
    """Load all COG modules."""
    extensions = [
        "commands.moderation",
        "commands.general",
        "commands.onboarding",
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
        # Создаём таблицы в БД (локально = SQLite, на Heroku = Postgres)
        Base.metadata.create_all(bind=engine)

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
