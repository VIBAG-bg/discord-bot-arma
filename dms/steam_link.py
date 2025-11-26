# dms/steam_link.py

import sys
import discord

from database.service import get_or_create_user, link_steam
from dms.localization import t


class SteamLinkModal(discord.ui.Modal):
    """Modal window to collect Steam ID from the user."""

    def __init__(self, member: discord.abc.User):
        user = get_or_create_user(member.id)
        lang = (user.language or "en") if user else "en"
        super().__init__(title=t(lang, "steam_modal_title"))
        self.member = member
        self.lang = lang

        self.steam_id_input = discord.ui.TextInput(
            label=t(lang, "steam_modal_label"),
            placeholder=t(lang, "steam_modal_placeholder"),
            max_length=32,
            required=True,
        )
        self.add_item(self.steam_id_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        try:
            if interaction.user.id != self.member.id:
                await interaction.response.send_message(
                    t(self.lang, "steam_modal_wrong_user"),
                    ephemeral=True,
                )
                return

            steam_id = self.steam_id_input.value.strip()

            user = get_or_create_user(self.member.id)
            lang = (user.language or "en") if user else "en"

            # Validate SteamID64 pattern
            if not (
                steam_id.isdigit()
                and len(steam_id) == 17
                and steam_id.startswith("7656119")
            ):
                await interaction.response.send_message(
                    t(lang, "invalid_steam_link"),
                    ephemeral=True,
                )
                return

            link_steam(discord_id=self.member.id, steam_id=steam_id)

            await interaction.response.send_message(
                t(lang, "steam_saved").format(steam_id=steam_id),
                ephemeral=True,
            )
        except Exception as e:
            print(f"[SteamLinkModal ERROR] {type(e).__name__}: {e}", file=sys.stderr)
            try:
                await interaction.response.send_message(
                    t(self.lang, "steam_modal_error"),
                    ephemeral=True,
                )
            except discord.InteractionResponded:
                pass


class LinkSteamButton(discord.ui.Button):
    """Button to open the SteamLinkModal."""
    def __init__(self, lang: str):
        super().__init__(
            label=t(lang, "btn_steam"),
            style=discord.ButtonStyle.primary,
            custom_id="link_steam_modal",
        )
        self.lang = lang

    async def callback(self, interaction: discord.Interaction):
        modal = SteamLinkModal(member=interaction.user)
        await interaction.response.send_modal(modal)


class SteamLinkView(discord.ui.View):
    """View with a button to start the Steam ID linking modal in DM or onboarding flow."""

    def __init__(self, lang: str):
        super().__init__(timeout=900)
        self.add_item(LinkSteamButton(lang))
