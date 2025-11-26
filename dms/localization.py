# dms/localization.py

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
        "onboarding_guild_only": "This command must be used in a server channel, not in DMs.",
        "onboarding_dm_sent_self": "Onboarding DM has been sent to you.",
        "onboarding_dm_failed_self": (
            "I couldn't send you a DM. Please enable DMs from server members and try again."
        ),
        "onboarding_dm_sent_other": "Onboarding DM has been sent to {member}.",
        "onboarding_dm_failed_other": "I couldn't DM {member}. Their DMs may still be disabled.",
        "steam_link": (
            "⚠️ You must link your Steam ID before applying as a recruit.\n\n"
            "Use the button below and enter your 17-digit SteamID64."
        ),
        "invalid_steam_link": (
            "This does not look like a valid SteamID64.\n"
            "Open your Steam profile → right click on profile page → "
            "\"Copy Page URL\" → take the long number at the end."
        ),
        "steam_saved": "Steam ID **{steam_id}** saved. Thank you!",
        "ping_title": "Pong!",
        "ping_description": "Bot latency: **{latency}ms**",
        "info_title": "Bot Information",
        "info_description": "ARMA 3 Community Discord Bot",
        "info_field_bot": "Bot",
        "info_field_servers": "Servers",
        "info_field_users": "Users",
        "info_field_uptime": "Uptime",
        "info_uptime_value": "{hours}h {minutes}m {seconds}s",
        "info_field_python_version": "Python Version",
        "info_field_discordpy_version": "discord.py Version",
        "requested_by": "Requested by {requester}",
        "serverinfo_title": "Server Information: {name}",
        "serverinfo_owner": "Owner",
        "serverinfo_members": "Members",
        "serverinfo_channels": "Channels",
        "serverinfo_channels_value": "Text: {text} | Voice: {voice}",
        "serverinfo_roles": "Roles",
        "serverinfo_id": "Server ID",
        "serverinfo_created_at": "Created At",
        "unknown_value": "Unknown",
        "userinfo_title": "User Information",
        "userinfo_name": "Name",
        "userinfo_nickname": "Nickname",
        "userinfo_no_nickname": "None",
        "userinfo_id": "User ID",
        "userinfo_status": "Status",
        "userinfo_joined": "Joined Server",
        "userinfo_created": "Account Created",
        "userinfo_roles_title": "Roles [{count}]",
        "roles_count_only": "{count} roles",
        "avatar_title": "{name}'s Avatar",
        "avatar_download_links": "Download Links",
        "avatar_download_links_value": "[PNG]({png}) | [JPG]({jpg}) | [WEBP]({webp})",
        "avatar_no_custom": "This user has no custom avatar.",
        "say_nothing_to_send": "Nothing to send.",
        "recruit_embed_title": "Recruit {name} ready for interview",
        "recruit_embed_status_ready": "READY FOR INTERVIEW",
        "recruit_already_applied": (
            "You have already applied as a recruit. "
            "If something seems wrong, contact the staff."
        ),
        "recruit_role_not_configured": (
            "Recruit role ID is not configured correctly. "
            "Please contact the staff."
        ),
        "recruit_role_not_found": (
            "Recruit role not found on the server. "
            "Ask the staff to configure it."
        ),
        "recruit_already_has_role": "You are already registered as a recruit.",
        "recruit_cannot_grant_role": (
            "I cannot grant the recruit role. "
            "Please contact the staff; I may be missing permissions."
        ),
        "game_role_not_found": "Configured role not found on server.",
        "no_permission_manage_roles": "I don't have permission to manage your roles.",

        # Onboarding
        "onboarding_title": "Welcome to the ARMA 3 tactical community",
        "onboarding_body": (
            "We focus on coordination, discipline and joint operations.\n"
            "Use the buttons below to set up your profile:"
        ),
        "btn_games": "Game roles",
        "btn_recruit": "Become a recruit",
        "btn_steam": "Link Steam ID",

        # Game roles
        "game_roles_title": "Choose your game roles",
        "game_roles_body": "Click a button to toggle a role. Click again to remove it.",
        "game_role_added": "Role **{role}** added.",
        "game_role_removed": "Role **{role}** removed.",
        "no_game_roles": "No game roles are configured yet.",

        "game_roles_panel_title": "Game roles",
        "game_roles_panel_body": (
            "Press the button below to open the game roles menu.\n"
            "In that menu you can enable or disable roles by clicking the buttons."
        ),

        # Errors
        "guild_not_found": "Server not found. Contact staff.",
        "not_in_guild": "I cannot find you on the server. Rejoin or contact staff.",

        "role_panel_title": "Role selection",
        "role_panel_body": (
            "Here you can select game roles, ARMA operation specializations "
            "and start the recruit process."
        ),
        "role_panel_games_header": "Game roles",
        "role_panel_arma_header": "ARMA operation specializations",

        "btn_games_panel": "Select game role",
        "btn_arma_panel": "Select ARMA role",

        "no_roles_configured": "No roles are configured in the bot config.",
        "no_arma_roles": "No ARMA operation roles are configured.",

        "arma_roles_title": "ARMA operation roles",
        "arma_roles_body": (
            "These roles are available only for approved recruits (status DONE).\n"
            "Use them to indicate your preferred roles during operations."
        ),
        "arma_roles_not_done": (
            "ARMA operation roles are only available for recruits with status **DONE**.\n"
            "Complete the recruit process first, then return to this panel."
        ),
        "arma_role_not_found": "This ARMA role is not configured or no longer exists.",
        "arma_role_added": "ARMA role **{role}** has been assigned.",
        "arma_role_removed": "ARMA role **{role}** has been removed.",
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
        "onboarding_guild_only": "Эту команду нужно использовать в канале сервера, а не в личных сообщениях.",
        "onboarding_dm_sent_self": "Онбординг-сообщение отправлено вам в личку.",
        "onboarding_dm_failed_self": (
            "Не удалось отправить вам личное сообщение. Включите ЛС от участников сервера и попробуйте снова."
        ),
        "onboarding_dm_sent_other": "Онбординг-сообщение отправлено {member}.",
        "onboarding_dm_failed_other": "Не удалось написать {member} в личные сообщения. Их ЛС, возможно, отключены.",
        "steam_link": (
            "⚠️ Перед тем как подать заявку рекрута, нужно привязать Steam ID.\n\n"
            "Используй кнопку ниже и введи свой 17-значный SteamID64."
        ),
        "invalid_steam_link": (
            "Это не похоже на корректный SteamID64.\n"
            "Откройте свой профиль в Steam → нажмите ПКМ по странице профиля → "
            "«Копировать URL-адрес» → возьмите длинное число в конце."
        ),
        "steam_saved": "Steam ID **{steam_id}** сохранён. Спасибо!",
        "ping_title": "Понг!",
        "ping_description": "Задержка бота: **{latency} мс**",
        "info_title": "Информация о боте",
        "info_description": "Discord-бот сообщества ARMA 3",
        "info_field_bot": "Бот",
        "info_field_servers": "Серверы",
        "info_field_users": "Пользователи",
        "info_field_uptime": "Время работы",
        "info_uptime_value": "{hours}ч {minutes}м {seconds}с",
        "info_field_python_version": "Версия Python",
        "info_field_discordpy_version": "Версия discord.py",
        "requested_by": "Запрошено пользователем {requester}",
        "serverinfo_title": "Информация о сервере: {name}",
        "serverinfo_owner": "Владелец",
        "serverinfo_members": "Участники",
        "serverinfo_channels": "Каналы",
        "serverinfo_channels_value": "Текст: {text} | Голос: {voice}",
        "serverinfo_roles": "Роли",
        "serverinfo_id": "ID сервера",
        "serverinfo_created_at": "Создан",
        "unknown_value": "Неизвестно",
        "userinfo_title": "Информация о пользователе",
        "userinfo_name": "Имя",
        "userinfo_nickname": "Никнейм",
        "userinfo_no_nickname": "Отсутствует",
        "userinfo_id": "ID пользователя",
        "userinfo_status": "Статус",
        "userinfo_joined": "Присоединился к серверу",
        "userinfo_created": "Аккаунт создан",
        "userinfo_roles_title": "Роли [{count}]",
        "roles_count_only": "{count} ролей",
        "avatar_title": "Аватар пользователя {name}",
        "avatar_download_links": "Ссылки для скачивания",
        "avatar_download_links_value": "[PNG]({png}) | [JPG]({jpg}) | [WEBP]({webp})",
        "avatar_no_custom": "У этого пользователя нет собственного аватара.",
        "say_nothing_to_send": "Нет текста для отправки.",
        "recruit_embed_title": "Рекрут {name} готов к собеседованию",
        "recruit_embed_status_ready": "READY FOR INTERVIEW",
        "recruit_already_applied": (
            "Ты уже подал заявку как рекрут. "
            "Если что-то не так, напиши рекрутёрам или модераторам."
        ),
        "recruit_role_not_configured": (
            "ID роли рекрута настроен некорректно. "
            "Сообщи, пожалуйста, администрации сервера."
        ),
        "recruit_role_not_found": (
            "Роль рекрута не найдена на сервере. "
            "Сообщи, пожалуйста, администрации сервера."
        ),
        "recruit_already_has_role": "Ты уже зарегистрирован как рекрут.",
        "recruit_cannot_grant_role": (
            "Я не могу выдать роль рекрута. "
            "Похоже, не хватает прав. Обратись к администрации."
        ),
        "game_role_not_found": "Настроенная игровая роль не найдена на сервере.",
        "no_permission_manage_roles": "У меня нет прав управлять твоими ролями.",

        # Новый онбординг
        "onboarding_title": "Добро пожаловать в наше тактическое сообщество ARMA 3",
        "onboarding_body": (
            "Мы делаем упор на координацию, дисциплину и совместные операции.\n"
            "Используйте кнопки ниже, чтобы настроить свой профиль:"
        ),
        "btn_games": "Игровые роли",
        "btn_recruit": "Стать рекрутом",
        "btn_steam": "Привязать Steam ID",

        # Игровые роли
        "game_roles_title": "Выбор игровых ролей",
        "game_roles_body": "Нажимайте на кнопки, чтобы получить или снять роль.",
        "game_role_added": "Роль **{role}** выдана.",
        "game_role_removed": "Роль **{role}** снята.",
        "no_game_roles": "Игровые роли ещё не настроены.",

        "game_roles_panel_title": "Игровые роли",
        "game_roles_panel_body": (
            "Нажми кнопку ниже, чтобы открыть меню игровых ролей.\n"
            "В нём можно включать и отключать роли по кнопкам."
        ),

        # Ошибки
        "guild_not_found": "Сервер не найден. Обратись к администрации.",
        "not_in_guild": "Я не могу найти тебя на сервере. Перезайди или напиши модераторам.",

        "role_panel_title": "Панель ролей",
        "role_panel_body": (
            "Здесь можно выбрать игровые роли, специализации для АРМА-операций "
            "и запустить процесс рекрутинга."
        ),
        "role_panel_games_header": "Игровые роли",
        "role_panel_arma_header": "Роли для АРМА-операций",

        "btn_games_panel": "Получить роль игры",
        "btn_arma_panel": "Получить роль по АРМЕ",

        "no_roles_configured": "В конфиге бота не настроены роли.",
        "no_arma_roles": "Роли для АРМА-операций не настроены.",

        "arma_roles_title": "Роли для АРМА-операций",
        "arma_roles_body": (
            "Эти роли доступны только одобренным рекрутам (статус DONE).\n"
            "Используются для обозначения желаемой роли на операциях."
        ),
        "arma_roles_not_done": (
            "Роли по АРМА-должностям доступны только рекрутам со статусом **DONE**.\n"
            "Сначала завершите рекрут-процесс, затем вернитесь к этой панели."
        ),
        "arma_role_not_found": "Эта роль для АРМА-операций не настроена или была удалена.",
        "arma_role_added": "Роль для АРМА-операций **{role}** выдана.",
        "arma_role_removed": "Роль для АРМА-операций **{role}** снята.",
    },
}


def t(lang: str, key: str) -> str:
    """Simple translation helper."""
    data = LANGS.get(lang) or LANGS["en"]
    return data.get(key) or LANGS["en"].get(key, key)
