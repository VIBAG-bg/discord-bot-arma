# dms/onboarding.py

import sys
import discord
from discord.ext import commands

from config import Config
from database.service import (
    link_steam,
    set_language,
    get_or_create_user,
    get_or_create_user_from_member,
    update_discord_profile,
    set_recruit_status,
    get_recruit_code,
    set_recruit_channels,
)

# ------------ LOCALIZATION ------------

LANGS = {
    "en": {
        "greeting": "Hello, {name}!",
        "roles_header": "Available server roles:",
        "roles_hint": "Press role buttons below to assign them instantly.",
        "recruit_hint": (
            "To register as an ARMA 3 recruit:\n"
            "→ Press the green 'Register as Recruit' button."
        ),
        "steam_intro": (
            "To complete your onboarding, please link your Steam account.\n\n"
            "How to find your SteamID64:\n"
            "1) Open Steam (client or browser) and go to your profile page.\n"
            "2) Right click on the page → 'Copy Page URL'.\n"
            "3) In the URL, there will be a long number at the end – this is your SteamID64.\n\n"
            "Press the **Link Steam ID** button below and paste this number into the form."
        ),
        "language_set": "Language set: EN",
        "choose_language": "Choose your language:",
        "steam_link": (
            "❗ You must link your Steam ID before applying as a recruit.\n"
            "Open your onboarding DM and fill in the Steam ID form.\n"
        ),
        "invalid_steam_link": (
            "This does not look like a valid SteamID64.\n"
            "Open your Steam profile → right click on profile page → "
            "\"Copy Page URL\" → take the long number at the end."
        ),
        "steam_saved": "Steam ID **{steam_id}** saved. Thank you!",
        "recruit_embed_title": "Recruit {name} ready for interview",
        "recruit_embed_status_ready": "READY FOR INTERVIEW",
    },
    "ru": {
        "greeting": "Привет, {name}!",
        "roles_header": "Доступные роли на сервере:",
        "roles_hint": "Нажмите на кнопки ролей ниже, чтобы выдать их себе.",
        "recruit_hint": (
            "Чтобы зарегистрироваться рекрутом ARMA 3:\n"
            "→ Нажмите зелёную кнопку «Register as Recruit»."
        ),
        "steam_intro": (
            "Чтобы завершить онбординг, привяжите ваш Steam-аккаунт.\n\n"
            "Как найти SteamID64:\n"
            "1) Откройте Steam и перейдите на страницу профиля.\n"
            "2) Нажмите ПКМ по странице → «Копировать URL-адрес».\n"
            "3) В конце ссылки будет длинное число — это ваш SteamID64.\n\n"
            "Нажмите кнопку **Link Steam ID** ниже и вставьте это число в форму."
        ),
        "language_set": "Язык установлен: RU",
        "choose_language": "Выберите язык:",
        "steam_link": (
            "❗ Сначала нужно привязать Steam ID, прежде чем подавать заявку рекрута.\n"
            "Открой личное сообщение с ботом и заполни форму Steam ID."
        ),
        "invalid_steam_link": (
            "Это не похоже на корректный SteamID64.\n"
            "Откройте свой профиль в Steam → нажмите ПКМ по странице профиля → "
            "«Копировать URL-адрес» → возьмите длинное число в конце."
        ),
        "steam_saved": "Steam ID **{steam_id}** сохранён. Спасибо!",
        "recruit_embed_title": "Рекрут {name} готов к собеседованию",
        "recruit_embed_status_ready": "ГОТОВ К СОБЕСЕДОВАНИЮ",
    },
}


def t(lang: str, key: str) -> str:
    """Simple translation helper."""
    data = LANGS.get(lang) or LANGS["en"]
    return data.get(key) or LANGS["en"].get(key, "")


# ------------ STEAM MODAL ------------


class SteamLinkModal(discord.ui.Modal):
    """Modal window to collect Steam ID from the user."""

    def __init__(self, member: discord.abc.User):
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
        try:
            # защита от чужих сабмитов
            if interaction.user.id != self.member.id:
                await interaction.response.send_message(
                    "This form is bound to another user.",
                    ephemeral=True,
                )
                return

            steam_id = self.steam_id_input.value.strip()

            # достаём юзера и язык из БД
            user = get_or_create_user(self.member.id)
            lang = (user.language or "en") if user else "en"

            # строгая валидация SteamID64: 17 цифр, начинается с '7656119'
            if not (steam_id.isdigit() and len(steam_id) == 17 and steam_id.startswith("7656119")):
                await interaction.response.send_message(
                    t(lang, "invalid_steam_link"),
                    ephemeral=True,
                )
                return

            # сохраняем в базу
            link_steam(discord_id=self.member.id, steam_id=steam_id)

            await interaction.response.send_message(
                t(lang, "steam_saved").format(steam_id=steam_id),
                ephemeral=True,
            )
        except Exception as e:
            # логируем нормальную ошибку, чтобы не было "что-то пошло не так"
            print(f"[SteamLinkModal ERROR] {type(e).__name__}: {e}", file=sys.stderr)
            try:
                await interaction.response.send_message(
                    "Internal error while saving Steam ID. Contact staff.",
                    ephemeral=True,
                )
            except discord.InteractionResponded:
                # на всякий случай, если уже ответили
                pass


# ------------ ROLE / RECRUIT VIEW ------------


class RoleSelectionView(discord.ui.View):
    """Interactive role selection + recruit registration view."""

    def __init__(self, bot_client: commands.Bot, guild_id: int, lang: str):
        super().__init__(timeout=3600)
        self.bot = bot_client
        self.guild_id = guild_id
        self.lang = lang

        from dms.onboarding import _get_role_definitions_for_lang
        for role_cfg in _get_role_definitions_for_lang(lang):
            self.add_item(RoleButton(role_cfg))

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

RECRUIT_ROLE_ID = Config.RECRUIT_ROLE_ID

async def create_recruit_channels(guild: discord.Guild, member: discord.Member):
    """
    Создаём личный текстовый и голосовой каналы для рекрута.
    Возвращаем (text_channel, voice_channel).
    """
    # 1) Категория
    category = guild.get_channel(Config.RECRUIT_CATEGORY_ID)
    if category is None or not isinstance(category, discord.CategoryChannel):
        # если категории нет – лучше не продолжать, чтобы не плодить мусор в корне сервера
        raise RuntimeError("Recruit category is not configured correctly.")

    # 2) Пермишены
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(
            view_channel=False
        ),
        member: discord.PermissionOverwrite(
            view_channel=True,
            read_message_history=True,
            send_messages=True,
            connect=True,
            speak=True,
        ),
    }

    # добавляем STAFF / RECRUITERS
    for role_id in getattr(Config, "RECRUITER_ROLE_IDS", []):
        role = guild.get_role(role_id)
        if role is not None:
            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=True,
                connect=True,
                speak=True,
            )


    user = get_or_create_user_from_member(member)  # ORM user
    code = get_recruit_code(user)

    base_name = f"recruit-{member.name.lower()}-{code}"

    text_channel = await guild.create_text_channel(
        name=base_name,
        category=category,
        overwrites=overwrites,
        reason=f"Recruit interview channel for {member}",
    )

    voice_channel = await guild.create_voice_channel(
        name=base_name,
        category=category,
        overwrites=overwrites,
        reason=f"Recruit interview voice for {member}",
    )
    # сохраняем ID каналов в БД
    set_recruit_channels(
        discord_id=member.id,
        text_id=text_channel.id,
        voice_id=voice_channel.id,
    )

    return text_channel, voice_channel



# ------------ REGISTER RECRUIT BUTTON ------------


class RegisterRecruitButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Register as Recruit",
            style=discord.ButtonStyle.success,
            custom_id="register_recruit",
        )

    async def callback(self, interaction: discord.Interaction):
        view: RoleSelectionView = self.view  # type: ignore
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

        # актуализируем профиль и читаем язык
        user = get_or_create_user_from_member(member)
        lang = user.language or "en"

         # проверяем статус рекрута по БД, а не по роли
        status = (user.recruit_status or "pending").lower()
        if status in ("ready", "done"):
            await interaction.response.send_message(
                "You have already applied as a recruit. Contact staff if something is wrong."
                if lang == "en"
                else "Ты уже зарегистрирован как рекрут. Если что-то не так, напиши рекрутеру.",
                ephemeral=True,
            )
            return
        
        # если у пользователя уже есть привязанные каналы рекрута, не создаём дубликаты
        if user.recruit_text_channel_id or user.recruit_voice_channel_id:
            await interaction.response.send_message(
                "You have already applied as a recruit. Contact staff if something is wrong."
                if lang == "en"
                else "Ты уже зарегистрирован как рекрут. Если что-то не так, напиши рекрутерам.",
                ephemeral=True,
            )
            return
                

        # проверка Steam ID
        if not user.steam_id:
            await interaction.response.send_message(
                t(lang, "steam_link"),
                ephemeral=True,
            )
            return

        recruit_id = RECRUIT_ROLE_ID
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

        # статус в БД
        set_recruit_status(member.id, "ready")

        # создаём личные каналы
        try:
            text_ch, voice_ch = await create_recruit_channels(guild, member)
        except Exception as e:
            # если не удалось создать каналы – хотя бы скажем модерам в логах
            print(f"[recruit channels ERROR] {type(e).__name__}: {e}", file=sys.stderr)
            await interaction.response.send_message(
                "Recruit role assigned, but interview channels could not be created. "
                "Please contact staff.",
                ephemeral=True,
            )
            return
        
        # обновим user (чтобы точно быть в курсе статуса/каналов)
        user = get_or_create_user_from_member(member)
        lang = user.language or "en"

        # Стим-ссылка
        if getattr(user, "steam_url", None):
            steam_url = user.steam_url
        elif user.steam_id:
            steam_url = f"https://steamcommunity.com/profiles/{user.steam_id}"
        else:
            steam_url = None

        recruit_code = get_recruit_code(user)

        embed = discord.Embed(
            title=t(lang, "recruit_embed_title"),
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

        embed.add_field(
            name="Language",
            value=user.language or "en",
            inline=True,
        )

        embed.add_field(
            name="Status",
            value=t(lang, "recruit_embed_status_ready"),
            inline=True,
        )

        embed.set_footer(text="Use this channel to schedule and run the interview.")

        try:
            await text_ch.send(content=member.mention, embed=embed, allow_mentions=discord.AllowedMentions(users=True, roles=False, everyone=False ))
        except Exception as e:
            print(f"[RecruitEmbed ERROR] {type(e).__name__}: {e}", file=sys.stderr)


        # ответ рекруту в DM-контексте (interaction – из лички)
        await interaction.response.send_message(
            (
                f'Recruit role "{recruit_role.name}" assigned!\n'
                f'Your application status: **READY**.\n\n'
                f'A private interview text & voice channel have been created for you:\n'
                f'- Text: {text_ch.mention}\n'
                f'- Voice: {voice_ch.mention}'
            ),
            ephemeral=True,
        )



# ------------ STEAM LINK VIEW ------------


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


# ------------ LANGUAGE SELECT ------------


class LanguageSelectView(discord.ui.View):
    """First step: language selection."""

    def __init__(self, bot_client: commands.Bot, guild_id: int):
        super().__init__(timeout=900)
        self.bot = bot_client
        self.guild_id = guild_id
        self.add_item(LanguageButton("en", "English"))
        self.add_item(LanguageButton("ru", "Русский"))


class LanguageButton(discord.ui.Button):
    def __init__(self, code: str, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.code = code

    async def callback(self, interaction: discord.Interaction):
        view: LanguageSelectView = self.view  # type: ignore[assignment]

        # пишем язык в БД
        set_language(interaction.user.id, self.code)

        # подтверждение
        await interaction.response.send_message(
            t(self.code, "language_set"),
            ephemeral=True,
        )

        # ищем участника в гильдии
        guild = view.bot.get_guild(view.guild_id)
        if guild is None:
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            try:
                member = await guild.fetch_member(interaction.user.id)
            except discord.DiscordException:
                return

        # отправляем вторую и третью ДМки
        await send_role_and_steam_dms(bot=view.bot, member=member, lang=self.code)


# ------------ DM TEXT HELPERS ------------


def _get_role_definitions_for_lang(lang: str):
    """
    Аккуратно достаём дефиниции ролей, не падая,
    даже если в Config нет каких-то атрибутов.
    """
    base = getattr(Config, "ROLE_DEFINITIONS", None)
    eng = getattr(Config, "ROLE_DEFINITIONS_ENG", None)
    rus = getattr(Config, "ROLE_DEFINITIONS_RUS", None)

    if lang == "ru":
        return rus or base or eng or []
    else:
        return eng or base or rus or []


def _format_role_list(lang: str) -> str:
    defs = _get_role_definitions_for_lang(lang)
    if not defs:
        return "- No self-assignable roles are configured."

    lines = []
    for cfg in defs:
        label = cfg.get("label", "Role")
        desc = cfg.get("description", "")
        lines.append(f"- {label}: {desc}".rstrip())
    return "\n".join(lines)


def _build_onboarding_message(member: discord.Member, lang: str) -> str:
    return (
        f"{t(lang, 'greeting').format(name=member.display_name)}\n\n"
        f"{Config.WELCOME_MESSAGE_ENG if lang == 'en' else Config.WELCOME_MESSAGE_RUS}\n\n"
        f"{t(lang, 'roles_header')}\n"
        f"{_format_role_list(lang)}\n\n"
        f"{t(lang, 'roles_hint')}\n\n"
        f"{t(lang, 'recruit_hint')}\n"
    )


def _build_steam_message(member: discord.Member, lang: str) -> str:
    return t(lang, "steam_intro")


async def send_role_and_steam_dms(bot: commands.Bot, member: discord.Member, lang: str):
    """Send roles DM + Steam DM after language selection."""
    # 2-е сообщение: роли и рекрут
    await member.send(
        _build_onboarding_message(member, lang),
        view=RoleSelectionView(bot_client=bot, guild_id=member.guild.id, lang=lang),
    )

    # 3-е сообщение: про Steam + кнопка с модалкой
    await member.send(
        _build_steam_message(member, lang),
        view=SteamLinkView(),
    )


# ------------ PUBLIC ENTRYPOINTS ------------


async def send_onboarding_dm(bot: commands.Bot, member: discord.Member) -> bool:
    """First onboarding DM: language selection."""
    if member.bot or member.guild is None:
        return True

    try:
        # создаём пользователя, если ещё нет
        get_or_create_user(member.id)
        # сразу сохраняем юзернейм и ник
        update_discord_profile(member)

        text = f"{t('ru', 'choose_language')} / {t('en', 'choose_language')}"

        await member.send(
            text,
            view=LanguageSelectView(bot_client=bot, guild_id=member.guild.id),
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

    # проще всего — двуязычное сообщение
    await channel.send(
        f"{member.mention}, enable direct messages so I can send your onboarding instructions. "
        f"After this, please send the `!onboarding` command on the server."
    )
