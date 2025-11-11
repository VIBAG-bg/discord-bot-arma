# Discord Bot - ARMA 3 Community

A modular Discord bot built with Python and Discord.py for ARMA 3 community servers. This bot provides essential moderation commands and general utility features.

## Features

### Moderation Commands
- **!kick** - Kick members from the server
- **!ban** - Ban members from the server
- **!unban** - Unban members using their user ID
- **!clear** - Bulk delete messages (up to 100)
- **!mute** - Timeout members temporarily
- **!unmute** - Remove timeout from members

### General Commands
- **!ping** - Check bot latency
- **!info** - Display bot information
- **!serverinfo** - Display server information
- **!userinfo** - Display user information
- **!avatar** - Display user's avatar
- **!help** - Show all available commands

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- A Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VIBAG-bg/discord-bot-arma.git
   cd discord-bot-arma
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   
   Create a `.env` file in the root directory:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your bot token:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   COMMAND_PREFIX=!
   OWNER_ID=your_discord_user_id
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

## Getting a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under the "Token" section, click "Reset Token" to get your bot token
6. Copy the token and paste it in your `.env` file

## Bot Permissions

When inviting the bot to your server, make sure it has the following permissions:
- Read Messages/View Channels
- Send Messages
- Embed Links
- Attach Files
- Read Message History
- Manage Messages (for !clear command)
- Kick Members (for !kick command)
- Ban Members (for !ban and !unban commands)
- Moderate Members (for !mute and !unmute commands)

### Invite Link Generator
Use this URL structure to generate an invite link (replace CLIENT_ID with your bot's client ID):
```
https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=1099780063302&scope=bot%20applications.commands
```

## Project Structure

```
discord-bot-arma/
├── bot.py              # Main bot file
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .gitignore         # Git ignore file
├── commands/          # Command cogs directory
│   ├── __init__.py
│   ├── moderation.py  # Moderation commands
│   └── general.py     # General utility commands
└── README.md          # This file
```

## Usage Examples

### Moderation Commands

**Kick a member:**
```
!kick @username Spamming in chat
```

**Ban a member:**
```
!ban @username Repeated rule violations
```

**Unban a user (requires user ID):**
```
!unban 123456789012345678 Appeal accepted
```

**Clear messages:**
```
!clear 50
```

**Mute a member for 30 minutes:**
```
!mute @username 30 Inappropriate behavior
```

**Unmute a member:**
```
!unmute @username
```

### General Commands

**Check bot latency:**
```
!ping
```

**Get bot information:**
```
!info
```

**Get server information:**
```
!serverinfo
```

**Get user information:**
```
!userinfo @username
```

**Get user avatar:**
```
!avatar @username
```

## Customization

### Adding New Commands

1. Create a new file in the `commands/` directory or add to existing cogs
2. Define your commands using the `@commands.command()` decorator
3. Add the cog to the extensions list in `bot.py`

Example:
```python
@commands.command(name='example')
async def example_command(self, ctx):
    """Example command description."""
    await ctx.send("This is an example!")
```

### Modifying Bot Behavior

- **Change command prefix**: Edit `COMMAND_PREFIX` in your `.env` file
- **Modify bot status**: Edit the `on_ready()` function in `bot.py`
- **Add event handlers**: Add new `@bot.event` decorated functions in `bot.py`

## Troubleshooting

**Bot doesn't respond to commands:**
- Make sure the bot has permission to read and send messages in the channel
- Verify that message content intent is enabled in the Discord Developer Portal
- Check that the command prefix is correct

**Permission errors:**
- Ensure the bot's role is high enough in the role hierarchy
- Check that the bot has the required permissions enabled

**Bot won't start:**
- Verify your bot token is correct in the `.env` file
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

## Contributing

Feel free to fork this repository and submit pull requests for any improvements!

## License

This project is open source and available for use in your own Discord servers.

## Support

For issues or questions, please open an issue on GitHub.
