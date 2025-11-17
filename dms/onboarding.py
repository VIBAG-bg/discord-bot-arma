import sys
import discord
from discord.ext import commands

from config import Config
from database.service import link_steam


# ------------ STEAM MODAL ------------

class SteamLinkModal(discord.ui.Modal):
    """Modal window to collect Steam ID from the user."""

    def __init__(self, member: discord.Member):
        super().__init__(title="Link your Steam ID")
        self.member = member

        self.steam_id_input = discord.ui.TextInput(
            label="Your Steam ID / SteamID64",
            placeholder="Example: 7656119XXXXXXXXXX",
            max_length=32,
            required=True,
        )
        self.add_item(self.steam_id_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # Защита от чужих сабмитов
        if interaction.user.id != self.member.id:
            await interaction.response.send_message(
                "This form is bound to another user.",
                ephemeral=True,
            )
            return

        steam_id = self.steam_id_input.value.strip()

        # Простая проверка формата
        if not steam_id.isdigit() or len(steam_id) < 10:
            await interaction.response.send_message(
                "This does not look like a valid SteamID64.\n"
                "Open your Steam profile → right click on profile page → "
                "\"Copy Page URL\" → take the long number at the end.",
                ephemeral=True,
            )
            return

        # Сохраняем в БД
        link_steam(discord_id=self.member.id, steam_id=steam_id)

        await interaction.response.send_message(
            f"Steam ID **{steam_id}** saved. Thank you!",
            ephemeral=True,
        )


# ------------ ROLE / RECRUIT VIEW ------------

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


class RoleButton(discord.ui.Button):
    def __init__(self, role_cfg: dict):
        label = role_cfg.get("label", "Role")
        role_id = role_cfg.get("id", 0)

        super().__init__(
            label=label,
            style=discord.ButtonStyle.secondary,
            custom_id=f"role_{role_id or label}",
        )
        self.role_cfg = role_cfg

    async def callback(self, interaction: discord.Interaction):
        # Берём guild из view, а не из interaction (в DM его нет)
        view: RoleSelectionView = self.view  # type: ignore[assignment]
        guild = view.bot.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                "Server not found. Contact staff.",
                delete_after=20,
            )
            return

        role_id = self.role_cfg.get("id")
        if not role_id:
            await interaction.response.send_message(
                "This role is not configured properly.",
                delete_after=20,
            )
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            await interaction.response.send_message(
                "Cannot find your account on this server.",
                delete_after=20,
            )
            return

        role = guild.get_role(role_id)
        if not role:
            await interaction.response.send_message(
                "Role not found. Ask staff to configure it.",
                delete_after=20,
            )
            return

        if role in member.roles:
            await interaction.response.send_message(
                f'Role "{role.name}" is already assigned.',
                delete_after=20,
            )
            return

        try:
            await member.add_roles(role, reason="Self-assigned via onboarding DM")
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to add that role.",
                delete_after=20,
            )
            return

        await interaction.response.send_message(
            f'Role "{role.name}" added!',
            delete_after=20,
        )


class RegisterRecruitButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Register as Recruit",
            style=discord.ButtonStyle.success,
            custom_id="register_recruit",
        )

    async def callback(self, interaction: discord.Interaction):
        view: RoleSelectionView = self.view  # type: ignore[assignment]
        guild = view.bot.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                "Server not found right now.",
                delete_after=20,
            )
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            await interaction.response.send_message(
                "Cannot find your member record on this server.",
                delete_after=20,
            )
            return

        recruit_id = Config.RECRUIT_ROLE_ID
        if not recruit_id:
            await interaction.response.send_message(
                "Recruit role ID is not configured correctly.",
                delete_after=20,
            )
            return

        recruit_role = guild.get_role(recruit_id)
        if not recruit_role:
            await interaction.response.send_message(
                "Recruit role not found. Ask staff to configure it.",
                delete_after=20,
            )
            return

        if recruit_role in member.roles:
            await interaction.response.send_message(
                "You are already registered as a recruit.",
                delete_after=20,
            )
            return

        try:
            await member.add_roles(recruit_role, reason="Recruit registration")
        except discord.Forbidden:
            await interaction.response.send_message(
                "I cannot grant the recruit role. Contact staff.",
                delete_after=20,
            )
            return

        await interaction.response.send_message(
            f'Recruit role "{recruit_role.name}" assigned!',
            delete_after=20,
        )


# ------------ STEAM LINK VIEW (2-е сообщение) ------------

class SteamLinkView(discord.ui.View):
    """View with a single button that opens Steam link modal."""

    def __init__(self):
        super().__init__(timeout=900)
        self.add_item(LinkSteamButton())


class LinkSteamButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Link Steam ID",
            style=discord.ButtonStyle.primary,
            custom_id="link_steam",
        )

    async def callback(self, interaction: discord.Interaction):
        modal = SteamLinkModal(member=interaction.user)
        await interaction.response.send_modal(modal)


# ------------ DM ONBOARDING TEXTS ------------

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


def _build_steam_message(member: discord.Member) -> str:
    return (
        "To complete your onboarding, please link your Steam account.\n\n"
        "How to find your SteamID64:\n"
        "1) Open Steam (client or browser) and go to your profile page.\n"
        "2) Right click on the page → 'Copy Page URL'.\n"
        "3) In the URL, there will be a long number at the end – this is your SteamID64.\n\n"
        "Press the **Link Steam ID** button below and paste this number into the form."
    )


# ------------ PUBLIC FUNCTIONS ------------

async def send_onboarding_dm(bot: commands.Bot, member: discord.Member) -> bool:
    """Send onboarding DMs. Returns True on success."""
    if member.bot or member.guild is None:
        return True

    try:
        # 1-е сообщение: роли и рекрут
        await member.send(
            _build_onboarding_message(member),
            view=RoleSelectionView(bot_client=bot, guild_id=member.guild.id),
        )

        # 2-е сообщение: про Steam + кнопка с модалкой
        await member.send(
            _build_steam_message(member),
            view=SteamLinkView(),
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
        f"{member.mention}, enable direct messages so I can send your onboarding "
        f"instructions. After enabling, please send `!onboarding` command in the server."
    )

# ------------ END OF FILE ------------
