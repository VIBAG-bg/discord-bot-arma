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
        "steam_link": (
            "❗ You must link your Steam ID before applying as a recruit.\n"
            "Open your onboarding DM and use the Steam ID button.\n"
        ),
        "invalid_steam_link": (
            "This does not look like a valid SteamID64.\n"
            "Open your Steam profile → right click on profile page → "
            "\"Copy Page URL\" → take the long number at the end."
        ),
        "steam_saved": "Steam ID **{steam_id}** saved. Thank you!",
        "recruit_embed_title": "Recruit {name} ready for interview",
        "recruit_embed_status_ready": "READY FOR INTERVIEW",

        # Новый онбординг
        "onboarding_title": "Welcome to the ARMA 3 tactical community",
        "onboarding_body": (
            "We focus on coordination, discipline and joint operations.\n"
            "Use the buttons below to set up your profile:"
        ),
        "btn_games": "Game roles",
        "btn_recruit": "Register as Recruit",
        "btn_steam": "Link Steam ID",

        # Игровые роли
        "game_roles_title": "Choose your game roles",
        "game_roles_body": "Click a button to toggle a role. Click again to remove it.",
        "game_role_added": "Role **{role}** added.",
        "game_role_removed": "Role **{role}** removed.",
        "no_game_roles": "No game roles are configured yet.",

        # Ошибки
        "guild_not_found": "Server not found. Contact staff.",
        "not_in_guild": "I cannot find you on the server. Rejoin or contact staff.",
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
            "Открой личное сообщение с ботом и используй кнопку Steam ID."
        ),
        "invalid_steam_link": (
            "Это не похоже на корректный SteamID64.\n"
            "Откройте свой профиль в Steam → нажмите ПКМ по странице профиля → "
            "«Копировать URL-адрес» → возьмите длинное число в конце."
        ),
        "steam_saved": "Steam ID **{steam_id}** сохранён. Спасибо!",
        "recruit_embed_title": "Рекрут {name} готов к собеседованию",
        "recruit_embed_status_ready": "READY FOR INTERVIEW",

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
        "game_roles_body": "Нажимайте на кнопки, чтобы выдать или снять роль.",
        "game_role_added": "Роль **{role}** выдана.",
        "game_role_removed": "Роль **{role}** снята.",
        "no_game_roles": "Игровые роли ещё не настроены.",

        # Ошибки
        "guild_not_found": "Сервер не найден. Обратись к администрации.",
        "not_in_guild": "Я не могу найти тебя на сервере. Перезайди или напиши модераторам.",
    },
}


def t(lang: str, key: str) -> str:
    """Simple translation helper."""
    data = LANGS.get(lang) or LANGS["en"]
    return data.get(key) or LANGS["en"].get(key, key)
