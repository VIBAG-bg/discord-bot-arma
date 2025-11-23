# dms/localization.py
import typing as t

LANGS: dict[str, dict[str, str]] = {
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
        "recruit_embed_status_ready": "READY FOR INTERVIEW",
    },
}


def t(lang: str, key: str) -> str:
    """Simple translation helper."""
    data = LANGS.get(lang) or LANGS["en"]
    return data.get(key) or LANGS["en"].get(key, "")
