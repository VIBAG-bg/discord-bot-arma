import discord
from discord.ext import commands
from database.service import get_or_create_user_from_member
from dms.localization import t


class EmbedHelpCommand(commands.MinimalHelpCommand):
    DESCRIPTION_KEYS: dict[str, str] = {
        "ping": "help_desc_ping",
        "info": "help_desc_info",
        "serverinfo": "help_desc_serverinfo",
        "userinfo": "help_desc_userinfo",
        "avatar": "help_desc_avatar",
        "say": "help_desc_say",
        "onboarding": "help_desc_onboarding",
        "onboarding_for": "help_desc_onboarding_for",
        "recruit": "help_desc_recruit",
        "recruits": "help_desc_recruits",
        "user_update": "help_desc_user_update",
        "user_updates": "help_desc_user_updates",
        "role_panel": "help_desc_role_panel",
        "kick": "help_desc_kick",
        "ban": "help_desc_ban",
        "unban": "help_desc_unban",
        "clear": "help_desc_clear",
        "mute": "help_desc_mute",
        "unmute": "help_desc_unmute",
    }
    """
    Custom help command that:
    - formats command list into embeds,
    - shows full usage (including <@user>),
    - hides admin-only commands from non-admins.
    """

    def _get_prefix(self) -> str:
        """Return the invoked prefix, defaulting to '!' if context is missing."""
        if self.context is not None:
            return self.context.clean_prefix
        return "!"

    def get_command_signature(self, command: commands.Command) -> str:
        """
        Build the signature string for a command, e.g.:
        !onboarding_for <@user>
        """
        prefix = self._get_prefix()
        usage = command.usage or command.signature
        return f"{prefix}{command.qualified_name} {usage}".strip()

    def _get_command_description(self, command: commands.Command, lang: str) -> str:
        """Return a localized description for a command with fallback to its own help."""
        key = self.DESCRIPTION_KEYS.get(command.qualified_name)
        if key:
            text = t(lang, key)
            if text and text != key:
                return text
        return command.help or command.short_doc or t(lang, "no_description")

    async def send_bot_help(self, mapping):
        """
        Render the main help:
        - shows Admin commands separately,
        - then iterates through non-admin commands by cogs.
        """
        prefix = self._get_prefix()
        author = getattr(self.context, "author", None)
        lang = "en"
        if isinstance(author, discord.Member):
            user = get_or_create_user_from_member(author)
            lang = user.language or "en"

        embed = discord.Embed(
            title=t(lang, "help_title"),
            description=t(lang, "help_description").format(prefix=prefix),
        )

        admin_commands: list[commands.Command] = []

        # Collect commands marked admin_only
        for cog, command_list in mapping.items():
            filtered = await self.filter_commands(command_list, sort=True)
            if not filtered:
                continue

            for command in filtered:
                if command.extras.get("admin_only"):
                    admin_commands.append(command)

        # Show Admin commands
        if admin_commands:
            lines = []
            for command in admin_commands:
                sig = self.get_command_signature(command)
                lines.append(
                    t(lang, "help_command_line").format(
                        signature=sig,
                        description=self._get_command_description(command, lang),
                    )
                )

            embed.add_field(
                name=t(lang, "help_admin_commands"),
                value="\n".join(lines),
                inline=False,
            )

        # Show regular commands grouped by cog, excluding admin_only
        for cog, command_list in mapping.items():
            filtered = await self.filter_commands(command_list, sort=True)
            if not filtered:
                continue

            regular = [
                cmd for cmd in filtered
                if not cmd.extras.get("admin_only")
            ]
            if not regular:
                continue

            cog_name = cog.qualified_name if cog else t(lang, "help_general_category")
            value_lines = []
            for command in regular:
                sig = self.get_command_signature(command)
                value_lines.append(
                    t(lang, "help_command_line").format(
                        signature=sig,
                        description=self._get_command_description(command, lang),
                    )
                )

            if value_lines:
                embed.add_field(
                    name=cog_name,
                    value="\n".join(value_lines),
                    inline=False,
                )

        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_command_help(self, command: commands.Command):
        """Help for a specific command: !help onboarding_for"""
        sig = self.get_command_signature(command)
        author = getattr(self.context, "author", None)
        lang = "en"
        if isinstance(author, discord.Member):
            user = get_or_create_user_from_member(author)
            lang = user.language or "en"
        embed = discord.Embed(
            title=t(lang, "help_command_title").format(signature=sig),
            description=self._get_command_description(command, lang),
        )

        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        """Help for a specific cog: !help Onboarding"""
        commands_list = await self.filter_commands(cog.get_commands(), sort=True)
        if not commands_list:
            return

        author = getattr(self.context, "author", None)
        lang = "en"
        if isinstance(author, discord.Member):
            user = get_or_create_user_from_member(author)
            lang = user.language or "en"
        embed = discord.Embed(
            title=t(lang, "help_category_title").format(name=cog.qualified_name),
            description=cog.__doc__ or t(lang, "no_description"),
        )

        for command in commands_list:
            sig = self.get_command_signature(command)
            embed.add_field(
                name=sig,
                value=self._get_command_description(command, lang),
                inline=False,
            )

        destination = self.get_destination()
        await destination.send(embed=embed)
