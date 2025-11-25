# dms/recruit_moderation.py
import sys
import discord

from config import Config
from database.service import (
    get_or_create_user_from_member,
    get_recruit_code,
    set_recruit_status,
)
from dms.localization import t


class RecruitModerationView(discord.ui.View):
    """
    Кнопки для рекрутеров / модераторов:
    - Approve: принять рекрута, выдать основную роль, снять рекрут-роль, архивнуть канал
    - Deny: отклонить, снять рекрут-роль, закрыть доступ
    """

    def __init__(
        self,
        guild_id: int,
        recruit_id: int,
        text_channel_id: int,
        voice_channel_id: int,
    ):
        super().__init__(timeout=30 * 24 * 3600)
        self.guild_id = guild_id
        self.recruit_id = recruit_id
        self.text_channel_id = text_channel_id
        self.voice_channel_id = voice_channel_id

        self.message_id: int | None = None

        self.add_item(ApproveRecruitButton())
        self.add_item(DenyRecruitButton())

    async def check_moderator(self, interaction: discord.Interaction) -> bool:
        guild = interaction.guild
        if guild is None:
            guild = interaction.client.get_guild(self.guild_id)
        if guild is None:
            return False

        member = guild.get_member(interaction.user.id)
        if member is None:
            return False

        if member.guild_permissions.administrator or member.guild_permissions.manage_guild:
            return True

        recruiter_ids = set(getattr(Config, "RECRUITER_ROLE_IDS", []))
        if getattr(Config, "RECRUITER_ROLE_ID", 0):
            recruiter_ids.add(Config.RECRUITER_ROLE_ID)

        if any(r.id in recruiter_ids for r in member.roles):
            return True

        db_user = get_or_create_user_from_member(member)
        if getattr(db_user, "is_admin", False):
            return True

        return False

    async def _archive_or_lock_channels(
        self,
        guild: discord.Guild,
        recruit: discord.Member,
        reason: str,
        deny_access: bool,
    ):
        text_ch = guild.get_channel(self.text_channel_id)
        voice_ch = guild.get_channel(self.voice_channel_id)

        archive_cat = None
        archive_cat_id = int(getattr(Config, "RECRUIT_ARCHIVE_CATEGORY_ID", 0) or 0)
        if archive_cat_id:
            ch = guild.get_channel(archive_cat_id)
            if isinstance(ch, discord.CategoryChannel):
                archive_cat = ch

        if isinstance(text_ch, discord.TextChannel):
            new_name = f"{text_ch.name}-archived"
            await text_ch.edit(
                name=new_name[:100],
                category=archive_cat or text_ch.category,
                reason=reason,
            )
            if deny_access:
                await text_ch.set_permissions(
                    recruit,
                    overwrite=discord.PermissionOverwrite(view_channel=False),
                )

        if isinstance(voice_ch, discord.VoiceChannel):
            new_name = f"{voice_ch.name}-archived"
            await voice_ch.edit(
                name=new_name[:100],
                category=archive_cat or voice_ch.category,
                reason=reason,
            )
            if deny_access:
                await voice_ch.set_permissions(
                    recruit,
                    overwrite=discord.PermissionOverwrite(view_channel=False),
                )

    async def disable_buttons(self, interaction: discord.Interaction):
        """Выключаем кнопки в исходном сообщении с карточкой рекрута."""
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

        try:
            guild = interaction.guild or interaction.client.get_guild(self.guild_id)
            if guild is None:
                return

            channel = guild.get_channel(self.text_channel_id)
            if not isinstance(channel, discord.TextChannel):
                return

            if self.message_id:
                msg = await channel.fetch_message(self.message_id)
            else:
                msg = interaction.message

            if msg:
                await msg.edit(view=self)
        except Exception as e:
            print(
                f"[RecruitModerationView.disable_buttons ERROR] {type(e).__name__}: {e}",
                file=sys.stderr,
            )

    async def process_approve(self, interaction: discord.Interaction):
        guild = interaction.guild or interaction.client.get_guild(self.guild_id)
        if guild is None:
            await interaction.followup.send("Guild not found.", ephemeral=True)
            return

        recruit = guild.get_member(self.recruit_id)
        if recruit is None:
            await interaction.followup.send(
                "Recruit not found on the server.",
                ephemeral=True,
            )
            return
        
        db_user = get_or_create_user_from_member(recruit)
        lang = (db_user.language or "en") if db_user else "en"

        if not getattr(db_user, "steam_id", None):
            if lang == "ru":
                text = (
                    "У этого рекрута ещё не привязан **SteamID64**.\n\n"
                    "Попросите его открыть личные сообщения с ботом и нажать кнопку "
                    "**\"Link Steam ID\"** в сообщении онбординга.\n"
                    "После этого вы сможете одобрить заявку."
                )
            else:
                text = (
                    "This recruit has not linked their **SteamID64** yet.\n\n"
                    "Ask them to open their DMs with the bot and press the "
                    "**\"Link Steam ID\"** button in the onboarding message.\n"
                    "After that you can approve the application."
                )

            await interaction.followup.send(text, ephemeral=True)
            return

        set_recruit_status(self.recruit_id, "done")

        recruit_role = guild.get_role(Config.RECRUIT_ROLE_ID)
        if recruit_role and recruit_role in recruit.roles:
            await recruit.remove_roles(
                recruit_role, reason=f"Recruit approved by {interaction.user}"
            )

        member_role_id = int(getattr(Config, "MEMBER_ROLE_ID", 0) or 0)
        if member_role_id:
            member_role = guild.get_role(member_role_id)
            if member_role and member_role not in recruit.roles:
                await recruit.add_roles(
                    member_role, reason="Recruit approved – promoted to member"
                )

        await self._archive_or_lock_channels(
            guild,
            recruit,
            reason=f"Recruit approved by {interaction.user}",
            deny_access=True,
        )

        channel = guild.get_channel(self.text_channel_id)
        if isinstance(channel, discord.TextChannel):
            await channel.send(
                f"Recruit {recruit.mention} approved by {interaction.user.mention}."
            )

        db_user = get_or_create_user_from_member(recruit)
        lang = (db_user.language or "en") if db_user else "en"

        msg_en = (
            "Congratulations! Your recruit application has been approved. "
            "Now you are a full member and got your member role! Welcome aboard!"
        )
        msg_ru = (
            "Поздравляем! Ваша заявка рекрута была одобрена. "
            "Теперь вы полноценный участник и получили роль! Добро пожаловать в команду!"
        )

        try:
            await recruit.send(msg_en if lang == "en" else msg_ru)
        except discord.Forbidden:
            print(f"[Recruit DM] Cannot DM {recruit} (forbidden)", file=sys.stderr)
        except Exception as e:
            print(f"[Recruit DM ERROR] {type(e).__name__}: {e}", file=sys.stderr)

        await self.disable_buttons(interaction)
        await interaction.followup.send(
            "Recruit approved, channels archived.",
            ephemeral=True,
        )

    async def process_deny(self, interaction: discord.Interaction):
        guild = interaction.guild or interaction.client.get_guild(self.guild_id)
        if guild is None:
            await interaction.followup.send("Guild not found.", ephemeral=True)
            return

        recruit = guild.get_member(self.recruit_id)
        if recruit is None:
            await interaction.followup.send(
                "Recruit not found on the server.",
                ephemeral=True,
            )
            return

        set_recruit_status(self.recruit_id, "rejected")

        recruit_role = guild.get_role(Config.RECRUIT_ROLE_ID)
        if recruit_role and recruit_role in recruit.roles:
            await recruit.remove_roles(
                recruit_role, reason=f"Recruit rejected by {interaction.user}"
            )

        await self._archive_or_lock_channels(
            guild,
            recruit,
            reason=f"Recruit rejected by {interaction.user}",
            deny_access=True,
        )

        db_user = get_or_create_user_from_member(recruit)
        lang = (db_user.language or "en") if db_user else "en"

        msg_en = "Unfortunately, your recruit application has been rejected."
        msg_ru = "К сожалению, ваша заявка рекрута была отклонена."

        try:
            await recruit.send(msg_en if lang == "en" else msg_ru)
        except discord.Forbidden:
            print(f"[Recruit DM] Cannot DM {recruit} (forbidden)", file=sys.stderr)
        except Exception as e:
            print(f"[Recruit DM ERROR] {type(e).__name__}: {e}", file=sys.stderr)

        channel = guild.get_channel(self.text_channel_id)
        if isinstance(channel, discord.TextChannel):
            await channel.send(
                f"Recruit {recruit.mention} rejected by {interaction.user.mention}."
            )

        await self.disable_buttons(interaction)
        await interaction.followup.send(
            "Recruit denied, channels archived.",
            ephemeral=True,
        )


class ConfirmApproveView(discord.ui.View):
    def __init__(self, parent: RecruitModerationView, lang: str):
        super().__init__(timeout=60)
        self.parent = parent
        self.lang = lang

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        await self.parent.process_approve(interaction)
        try:
            text = "Approved." if self.lang == "en" else "Одобрено."
            await interaction.message.edit(content=text, view=None)
        except Exception:
            pass
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        text = "Cancelled." if self.lang == "en" else "Отменено."
        await interaction.response.edit_message(content=text, view=None)
        self.stop()


class ConfirmDenyView(discord.ui.View):
    def __init__(self, parent: RecruitModerationView, lang: str):
        super().__init__(timeout=60)
        self.parent = parent
        self.lang = lang

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.danger)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        await self.parent.process_deny(interaction)
        try:
            text = "Denied." if self.lang == "en" else "Отклонено."
            await interaction.message.edit(content=text, view=None)
        except Exception:
            pass
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.secondary)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        text = "Cancelled." if self.lang == "en" else "Отменено."
        await interaction.response.edit_message(content=text, view=None)
        self.stop()


class ApproveRecruitButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Approve",
            style=discord.ButtonStyle.success,
            custom_id="recruit_approve",
        )

    async def callback(self, interaction: discord.Interaction):
        view: RecruitModerationView = self.view  # type: ignore

        if not await view.check_moderator(interaction):
            await interaction.response.send_message(
                "You are not allowed to approve recruits.",
                ephemeral=True,
            )
            return

        guild = interaction.guild or interaction.client.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                "Guild not found.", ephemeral=True
            )
            return

        recruit = guild.get_member(view.recruit_id)
        if recruit is None:
            await interaction.response.send_message(
                "Recruit not found on the server.",
                ephemeral=True,
            )
            return

        db_user = get_or_create_user_from_member(recruit)
        lang = (db_user.language or "en") if db_user else "en"

        question = (
            f"Are you sure you want to **APPROVE** {recruit.mention}?"
            if lang == "en"
            else f"Вы уверены, что хотите **ОДОБРИТЬ** {recruit.mention}?"
        )

        confirm_view = ConfirmApproveView(parent=view, lang=lang)

        await interaction.response.send_message(
            question,
            view=confirm_view,
            ephemeral=True,
        )


class DenyRecruitButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Deny",
            style=discord.ButtonStyle.danger,
            custom_id="recruit_deny",
        )

    async def callback(self, interaction: discord.Interaction):
        view: RecruitModerationView = self.view  # type: ignore

        if not await view.check_moderator(interaction):
            await interaction.response.send_message(
                "You are not allowed to deny recruits.",
                ephemeral=True,
            )
            return

        guild = interaction.guild or interaction.client.get_guild(view.guild_id)
        if guild is None:
            await interaction.response.send_message(
                "Guild not found.", ephemeral=True
            )
            return

        recruit = guild.get_member(view.recruit_id)
        if recruit is None:
            await interaction.response.send_message(
                "Recruit not found on the server.",
                ephemeral=True,
            )
            return

        db_user = get_or_create_user_from_member(recruit)
        lang = (db_user.language or "en") if db_user else "en"

        question = (
            f"Are you sure you want to **DENY** {recruit.mention}?"
            if lang == "en"
            else f"Вы уверены, что хотите **ОТКЛОНИТЬ** {recruit.mention}?"
        )

        confirm_view = ConfirmDenyView(parent=view, lang=lang)

        await interaction.response.send_message(
            question,
            view=confirm_view,
            ephemeral=True,
        )


async def send_recruit_moderation_embed(
    guild: discord.Guild,
    member: discord.Member,
    text_ch: discord.TextChannel,
    voice_ch: discord.VoiceChannel,
):
    """
    Шлём в текстовый канал рекрута:
    - embed-карточку
    - view с кнопками Approve / Deny
    """
    user = get_or_create_user_from_member(member)
    lang = user.language or "en"

    if getattr(user, "steam_url", None):
        steam_url = user.steam_url
    elif user.steam_id:
        steam_url = f"https://steamcommunity.com/profiles/{user.steam_id}"
    else:
        steam_url = None

    recruit_code = get_recruit_code(user)

    embed = discord.Embed(
        title=t(lang, "recruit_embed_title").format(name=member.display_name),
        color=discord.Color.gold(),
    )

    embed.add_field(
        name="Recruit code",
        value=recruit_code,
        inline=False,
    )

    embed.add_field(
        name="Discord",
        value=(
            f"{member.mention}\n"
            f"Display name: **{member.display_name}**\n"
            f"Username: `{member.name}`\n"
            f"ID: `{member.id}`"
        ),
        inline=False,
    )

    if steam_url:
        embed.add_field(
            name="Steam",
            value=f"ID: `{user.steam_id}`\n[Open profile]({steam_url})",
            inline=False,
        )
    else:
        embed.add_field(
            name="Steam",
            value="Not linked",
            inline=False,
        )

    lang_name = {
        "ru": "Русский",
        "en": "English",
    }.get(user.language, "English")

    embed.add_field(
        name="Language",
        value=lang_name,
        inline=True,
    )

    embed.add_field(
        name="Status",
        value=t(lang, "recruit_embed_status_ready"),
        inline=True,
    )

    embed.set_footer(text="Use this channel to schedule and run the interview.")

    role = guild.get_role(Config.RECRUITER_ROLE_ID)
    content = f"{member.mention} {role.mention}" if role else member.mention

    mod_view = RecruitModerationView(
        guild_id=guild.id,
        recruit_id=member.id,
        text_channel_id=text_ch.id,
        voice_channel_id=voice_ch.id,
    )

    try:
        msg = await text_ch.send(
            content=content,
            embed=embed,
            view=mod_view,
            allowed_mentions=discord.AllowedMentions(users=True, roles=True),
        )
        mod_view.message_id = msg.id
    except Exception as e:
        print(f"[RecruitEmbed ERROR] {type(e).__name__}: {e}", file=sys.stderr)
