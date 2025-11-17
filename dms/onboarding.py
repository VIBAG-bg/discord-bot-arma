import sys
import discord
from discord.ext import commands
from config import Config


class RoleSelectionView(discord.ui.View):
    """Interactive role selection + recruit registration view."""

    def __init__(self, bot_client: commands.Bot, guild_id: int):
        super().__init__(timeout=3600)
        self.bot = bot_client
        self.guild_id = guild_id

        # Role buttons
        for role_cfg in Config.ROLE_DEFINITIONS:
            self.add_item(RoleButton(role_cfg))

        # Recruit button
        self.add_item(RegisterRecruitButton())


# ------------ BUTTONS ------------

class RoleButton(discord.ui.Button):
    def __init__(self, role_cfg: dict):
        label = role_cfg.get("label", "Role")
        role_id = role_cfg.get("id", 0)

        super().__init__(
            label=label,
            style=discord.ButtonStyle.secondary,
            custom_id=f"role_{role_id or label}"
        )
        self.role_cfg = role_cfg

    async def callback(self, interaction: discord.Interaction):
        # Берём guild из view, а не из interaction (в DM его нет)
        view: RoleSelectionView = self.view  # type: ignore[assignment]
        guild = view.bot.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                "Server not found. Contact staff.",
                delete_after=20
            )
            return

        role_id = self.role_cfg.get("id")
        if not role_id:
            await interaction.response.send_message(
                "This role is not configured properly.",
                delete_after=20
            )
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            await interaction.response.send_message(
                "Cannot find your account on this server.",
                delete_after=20
            )
            return

        role = guild.get_role(role_id)
        if not role:
            await interaction.response.send_message(
                "Role not found. Ask staff to configure it.",
                delete_after=20
            )
            return

        if role in member.roles:
            await interaction.response.send_message(
                f'Role "{role.name}" is already assigned.',
                delete_after=20
            )
            return

        try:
            await member.add_roles(role, reason="Self-assigned via onboarding DM")
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to add that role.",
                delete_after=20
            )
            return

        await interaction.response.send_message(
            f'Role "{role.name}" added!',
            delete_after=20
        )


class RegisterRecruitButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Register as Recruit",
            style=discord.ButtonStyle.success,
            custom_id="register_recruit"
        )

    async def callback(self, interaction: discord.Interaction):
        view: RoleSelectionView = self.view  # type: ignore[assignment]
        guild = view.bot.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                "Server not found right now.",
                delete_after=20
            )
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            await interaction.response.send_message(
                "Cannot find your member record on this server.",
                delete_after=20
            )
            return

        recruit_id = Config.RECRUIT_ROLE_ID
        if not recruit_id:
            await interaction.response.send_message(
                "Recruit role ID is not configured correctly.",
                delete_after=20
            )
            return

        recruit_role = guild.get_role(recruit_id)
        if not recruit_role:
            await interaction.response.send_message(
                "Recruit role not found. Ask staff to configure it.",
                delete_after=20
            )
            return

        if recruit_role in member.roles:
            await interaction.response.send_message(
                "You are already registered as a recruit.",
                delete_after=20
            )
            return

        try:
            await member.add_roles(recruit_role, reason="Recruit registration")
        except discord.Forbidden:
            await interaction.response.send_message(
                "I cannot grant the recruit role. Contact staff.",
                delete_after=20
            )
            return

        await interaction.response.send_message(
            f'Recruit role "{recruit_role.name}" assigned!',
            delete_after=20
        )


# ------------ DM ONBOARDING LOGIC ------------

def _format_role_list() -> str:
    if not Config.ROLE_DEFINITIONS:
        return "- No self-assignable roles are configured."

    lines = []
    for cfg in Config.ROLE_DEFINITIONS:
        label = cfg.get("label", "Role")
        desc = cfg.get("description", "")
        lines.append(f"- {label}: {desc}".rstrip())
    return "\n".join(lines)


def _build_onboarding_message(member: discord.Member) -> str:
    return (
        f"Hello, {member.display_name}!\n\n"
        f"{Config.WELCOME_MESSAGE}\n\n"
        f"Available server roles:\n"
        f"{_format_role_list()}\n\n"
        "Press role buttons below to assign them instantly.\n\n"
        "To register as an ARMA 3 recruit:\n"
        "→ Press the green 'Register as Recruit' button.\n"
    )


async def send_onboarding_dm(bot: commands.Bot, member: discord.Member) -> bool:
    """Send onboarding DM. Returns True on success."""
    if member.bot or member.guild is None:
        return True

    try:
        await member.send(
            _build_onboarding_message(member),
            view=RoleSelectionView(bot_client=bot, guild_id=member.guild.id)
        )
        return True
    except discord.Forbidden:
        return False
    except discord.HTTPException as e:
        print(f"Failed to send DM: {e}", file=sys.stderr)
        return False


async def notify_dm_disabled(bot: commands.Bot, member: discord.Member):
    """Notify fallback channel if user's DM is blocked."""
    chan_id = Config.FALLBACK_CHANNEL_ID
    if not chan_id:
        return

    channel = bot.get_channel(chan_id)
    if channel is None:
        try:
            channel = await bot.fetch_channel(chan_id)
        except Exception as e:
            print(f"Cannot fetch fallback channel: {e}", file=sys.stderr)
            return

    await channel.send(
        f"{member.mention}, enable direct messages so I can send your onboarding instructions. After enabling, please send `!onboarding` command in the server."
    )
# ------------ END OF FILE ------------