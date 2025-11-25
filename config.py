import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Bot configuration class."""

    _raw_db_url = os.getenv("DATABASE_URL")

    # Хероку даёт postgres://, SQLAlchemy хочет postgresql+psycopg2://
    if _raw_db_url and _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql+psycopg2://", 1)

    # ФИНАЛЬНЫЙ URL
    DATABASE_URL = _raw_db_url or "sqlite:///bot.db"




    # Discord bot token (required)
    TOKEN: str | None = os.getenv("DISCORD_TOKEN")

    # Command prefix
    PREFIX: str = os.getenv("COMMAND_PREFIX", "!")

    # Bot owner ID (optional)
    OWNER_ID: int | None = (
        int(os.getenv("OWNER_ID")) if os.getenv("OWNER_ID") else None
    )

    # Welcome/onboarding text used in DM greeting
    WELCOME_MESSAGE_ENG: str = os.getenv(
        "WELCOME_MESSAGE",
        (
            "Welcome to the ARMA 3 tactical community. We focus on coordination, "
            "discipline, and joint operations. Before we deploy, please choose your roles "
            "and register as a recruit so the staff can learn your interests and prepare "
            "you for upcoming missions."
        ),
    )

    WELCOME_MESSAGE_RUS: str = os.getenv(
        "WELCOME_MESSAGE_RUS",
        (
            "Добро пожаловать в тактическое сообщество ARMA 3. "
            "Мы уделяем особое внимание координации, дисциплине и совместным операциям. "
            "Перед началом выберите свои роли и зарегистрируйтесь в качестве новобранца, "
            "чтобы персонал мог узнать о ваших интересах и подготовить вас к предстоящим миссиям."
        ),
    )

    # Discord channel ID used as fallback when a DM cannot be delivered
    FALLBACK_CHANNEL_ID: int = int(os.getenv("FALLBACK_CHANNEL_ID", "0"))

        # Язык по умолчанию для серверных панелей (role_panel и т.п.)
    DEFAULT_LANG: str = os.getenv("DEFAULT_LANG", "ru")

    # Игровые роли, которые можно выбирать через онбординг и !role_panel
    GAME_ROLE_DEFINITIONS: list[dict] = [
        {
            "id": int(os.getenv("GAME_ROLE_ARMA3_ID", "0")),
            "label_en": "ARMA 3",
            "label_ru": "ARMA 3",
            "description_en": "Tactical military simulation game.",
            "description_ru": "Тактический военный симулятор.",
            "emoji": "🎯",
        },
        {
            "id": int(os.getenv("GAME_ROLE_SQUAD_ID", "0")),
            "label_en": "Squad",
            "label_ru": "Squad",
            "description_en": "Team-based military FPS game.",
            "description_ru": "Командный военный шутер от первого лица.",
            "emoji": "🪖",
        },
        {
            "id": int(os.getenv("GAME_ROLE_CSGO_ID", "0")),
            "label_en": "CS GO",
            "label_ru": "CS GO",
            "description_en": "Competitive first-person shooter game.",
            "description_ru": "Конкурентный шутер от первого лица.",
            "emoji": "💥",
        },
        {
            "id": int(os.getenv("GAME_ROLE_MINECRAFT_ID", "0")),
            "label_en": "Minecraft",
            "label_ru": "Minecraft",
            "description_en": "Sandbox construction and survival game.",
            "description_ru": "Песочница для строительства и выживания.",
            "emoji": "⛏️",
        },
        {
            "id": int(os.getenv("GAME_ROLE_RUST_ID", "0")),
            "label_en": "Rust",
            "label_ru": "Rust",
            "description_en": "Survival game set in a post-apocalyptic world.",
            "description_ru": "Игра на выживание в постапокалиптическом мире.",
            "emoji": "🪓",
        },
        # добавь/убери по вкусу, главное: id, label_en/label_ru, emoji
    ]


    ARMA_ROLE_DEFINITIONS = [
    {
        "id": int(os.getenv("ARMA_ROLE_SQUAD_LEADER_ID", "0")),
        "label_en": "Squad Leader",
        "label_ru": "Командир отделения",
        "description_en": "Leads the squad, coordinates movement and communication.",
        "description_ru": "Руководит отделением, координирует передвижение и связь.",
        "emoji": "🎯",
    },
    {
        "id": int(os.getenv("ARMA_ROLE_TEAM_LEADER_ID", "0")),
        "label_en": "Team Leader",
        "label_ru": "Командир звена",
        "description_en": "Leads a fireteam during engagements.",
        "description_ru": "Управляет боевым звеном во время боевых действий.",
        "emoji": "🔱",
    },
    {
        "id": int(os.getenv("ARMA_ROLE_RIFLEMAN_ID", "0")),
        "label_en": "Rifleman",
        "label_ru": "Стрелок",
        "description_en": "Standard infantry role, main firepower of the squad.",
        "description_ru": "Базовая пехотная роль, главный носитель огневой мощи.",
        "emoji": "🔫",
    },
    {
        "id": int(os.getenv("ARMA_ROLE_MEDIC_ID", "0")),
        "label_en": "Medic",
        "label_ru": "Медик",
        "description_en": "Provides medical support and stabilizes injured teammates.",
        "description_ru": "Оказывает медицинскую помощь и стабилизирует раненых.",
        "emoji": "⛑️",
    },
    {
        "id": int(os.getenv("ARMA_ROLE_AUTORIFLEMAN_ID", "0")),
        "label_en": "Autorifleman",
        "label_ru": "Пулемётчик",
        "description_en": "Delivers suppressive fire using a machine gun.",
        "description_ru": "Ведёт подавляющий огонь из пулемёта.",
        "emoji": "🧨",
    },
    {
        "id": int(os.getenv("ARMA_ROLE_AT_SPECIALIST_ID", "0")),
        "label_en": "AT Specialist",
        "label_ru": "ПТ-специалист",
        "description_en": "Carries anti-tank weapons and engages armored vehicles.",
        "description_ru": "Использует противотанковое оружие, уничтожает бронетехнику.",
        "emoji": "🚀",
    },
    {
        "id": int(os.getenv("ARMA_ROLE_MARKSMAN_ID", "0")),
        "label_en": "Marksman",
        "label_ru": "Маркер / Дальнобойщик",
        "description_en": "Engages targets at medium-long distances with high accuracy.",
        "description_ru": "Атакует цели на средних и дальних дистанциях с высокой точностью.",
        "emoji": "🎯",
    },
    {
        "id": int(os.getenv("ARMA_ROLE_ENGINEER_ID", "0")),
        "label_en": "Engineer",
        "label_ru": "Инженер",
        "description_en": "Handles explosives, repairs vehicles, performs technical tasks.",
        "description_ru": "Работает с взрывчаткой, техникой и инженерными задачами.",
        "emoji": "🛠️",
    },
]


    # Recruit role ID (button "Register as Recruit")
    RECRUIT_ROLE_ID: int = int(os.getenv("RECRUIT_ROLE_ID", "0"))

    # Static list of roles that can be self-assigned via onboarding DM
    ROLE_DEFINITIONS_ENG: list[dict] = [
        {
            "label": "Assault",
            "description": "Frontline infantry focused on direct engagements.",
            "id": int(os.getenv("ROLE_ASSAULT_ID", "0")),
        },
        {
            "label": "Medic",
            "description": "Keeps squads alive with triage and evacuations.",
            "id": int(os.getenv("ROLE_MEDIC_ID", "0")),
        },
        {
            "label": "Pilot",
            "description": "Provides air transport, close air support, and logistics.",
            "id": int(os.getenv("ROLE_PILOT_ID", "0")),
        },
        {
            "label": "Support",
            "description": "Handles vehicles, heavy weapons, and resupply.",
            "id": int(os.getenv("ROLE_SUPPORT_ID", "0")),
        },
    ]

    ROLE_DEFINITIONS_RUS: list[dict] = [
        {
            "label": "Штурмовик",
            "description": "Пехота передовой, сосредоточенная на прямых столкновениях.",
            "id": int(os.getenv("ROLE_ASSAULT_ID", "0")),
        },
        {
            "label": "Медик",
            "description": "Поддерживает отряды живыми с помощью сортировки и эвакуации.",
            "id": int(os.getenv("ROLE_MEDIC_ID", "0")),
        },
        {
            "label": "Пилот",
            "description": "Обеспечивает воздушную транспортировку, поддержку с воздуха и логистику.",
            "id": int(os.getenv("ROLE_PILOT_ID", "0")),
        },
        {
            "label": "Поддержка",
            "description": "Обслуживает транспортные средства, тяжелое оружие и пополнение запасов.",
            "id": int(os.getenv("ROLE_SUPPORT_ID", "0")),
        },
    ]

    RECRUITER_ROLE_ID: int = int(os.getenv("RECRUITER_ROLE_ID") or "0")
    RECRUIT_CATEGORY_ID: int = int(os.getenv("RECRUIT_CATEGORY_ID") or "0")

    # основная роль участника, если хочешь её выдавать после approve
    MEMBER_ROLE_ID: int = int(os.getenv("MEMBER_ROLE_ID", "0"))

    # категория для архива рекрутов (необязательно, можно оставить 0)
    RECRUIT_ARCHIVE_CATEGORY_ID: int = int(os.getenv("RECRUIT_ARCHIVE_CATEGORY_ID", "0"))



    @staticmethod
    def validate() -> bool:
        """Validate that required configuration is present."""
        if not Config.TOKEN:
            raise ValueError("DISCORD_TOKEN is not set in .env file")
        return True
