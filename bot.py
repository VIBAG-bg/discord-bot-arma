"""
Main Discord Bot for ARMA 3 Community
A modular Discord bot built with discord.py
"""

import discord
from discord.ext import commands
import asyncio
import sys
from config import Config

# Configure bot intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content
intents.members = True  # Required for member-related events
intents.presences = False  # Can be disabled if not needed

# Initialize bot with command prefix and intents
bot = commands.Bot(
    command_prefix=Config.PREFIX,
    intents=intents,
    help_command=commands.DefaultHelpCommand(),
    description="ARMA 3 Community Discord Bot"
)


@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(f'Bot is ready!')
    print(f'Logged in as: {bot.user.name} (ID: {bot.user.id})')
    print(f'Discord.py version: {discord.__version__}')
    print(f'Connected to {len(bot.guilds)} guild(s)')
    print('------')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Game(name=f"{Config.PREFIX}help | ARMA 3")
    )


@bot.event
async def on_command_error(ctx, error):
    """Global error handler for commands."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Bad argument: {error}")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ This command is on cooldown. Try again in {error.retry_after:.2f}s")
    else:
        print(f'Error: {error}', file=sys.stderr)
        await ctx.send(f"❌ An error occurred while executing the command.")


@bot.event
async def on_member_join(member):
    """Event handler for when a new member joins the server."""
    # Find a general or welcome channel
    channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel:
        await channel.send(f'👋 Welcome to {member.guild.name}, {member.mention}!')


@bot.event
async def on_member_remove(member):
    """Event handler for when a member leaves the server."""
    channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel:
        await channel.send(f'👋 {member.name} has left the server.')


async def load_extensions():
    """Load all command cogs."""
    extensions = [
        'commands.moderation',
        'commands.general'
    ]
    
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f'Loaded extension: {extension}')
        except Exception as e:
            print(f'Failed to load extension {extension}: {e}', file=sys.stderr)


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
