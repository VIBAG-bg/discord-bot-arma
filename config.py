"""
Configuration module for Discord bot.
Handles loading environment variables and bot settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Bot configuration class."""
    
    # Discord Bot Token (Required)
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    # Command Prefix
    PREFIX = os.getenv('COMMAND_PREFIX', '/')
    
    # Bot Owner ID
    OWNER_ID = os.getenv('OWNER_ID')
    
    @staticmethod
    def validate():
        """Validate that required configuration is present."""
        if not Config.TOKEN:
            raise ValueError("DISCORD_TOKEN is not set in .env file")
        return True
