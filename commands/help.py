import discord
from discord.ext import commands


class EmbedHelpCommand(commands.MinimalHelpCommand):
    """
    Автоматический help, который:
    - показывает команды в embed'ах,
    - использует usage (типа <@user>),
    - выносит admin-команды в отдельный раздел.
    """

    def _get_prefix(self) -> str:
        """Безопасно получаем префикс, даже если контекста ещё нет."""
        if self.context is not None:
            return self.context.clean_prefix
        return "!"  # запасной вариант, хотя до него почти не дойдёт

    def get_command_signature(self, command: commands.Command) -> str:
        """
        Формируем красивую сигнатуру:
        !onboarding_for <@user>
        """
        prefix = self._get_prefix()
        usage = command.usage or command.signature
        return f"{prefix}{command.qualified_name} {usage}".strip()

    async def send_bot_help(self, mapping):
        """
        Главная страница help:
        - отдельный блок Admin commands,
        - ниже команды по категориям (cogs).
        """
        prefix = self._get_prefix()

        embed = discord.Embed(
            title="Help • ARMA 3 Bot",
            description=(
                "Список доступных команд.\n"
                f"Используй `{prefix}help <команда>` для подробностей."
            ),
        )

        admin_commands: list[commands.Command] = []

        # Собираем все admin_only команды
        for cog, command_list in mapping.items():
            filtered = await self.filter_commands(command_list, sort=True)
            if not filtered:
                continue

            for command in filtered:
                if command.extras.get("admin_only"):
                    admin_commands.append(command)

        # Добавляем блок Admin commands
        if admin_commands:
            lines = []
            for command in admin_commands:
                sig = self.get_command_signature(command)
                lines.append(f"`{sig}` — {command.short_doc or 'No description.'}")

            embed.add_field(
                name="🛡 Admin commands",
                value="\n".join(lines),
                inline=False,
            )

        # Обычные команды по категориям (cogs), без admin_only
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

            cog_name = cog.qualified_name if cog else "General"
            value_lines = []
            for command in regular:
                sig = self.get_command_signature(command)
                value_lines.append(
                    f"`{sig}` — {command.short_doc or 'No description.'}"
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
        """Help для конкретной команды: !help onboarding_for"""
        sig = self.get_command_signature(command)
        embed = discord.Embed(
            title=f"Command: {sig}",
            description=command.help or command.short_doc or "No description.",
        )

        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        """Help для конкретного cog'а: !help Onboarding"""
        commands_list = await self.filter_commands(cog.get_commands(), sort=True)
        if not commands_list:
            return

        embed = discord.Embed(
            title=f"Category: {cog.qualified_name}",
            description=cog.__doc__ or "No description.",
        )

        for command in commands_list:
            sig = self.get_command_signature(command)
            embed.add_field(
                name=sig,
                value=command.short_doc or "No description.",
                inline=False,
            )

        destination = self.get_destination()
        await destination.send(embed=embed)
