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
