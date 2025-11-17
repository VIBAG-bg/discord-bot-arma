import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Bot configuration class."""

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
    ROLE_DEFINITIONS: list[dict] = [
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

    @staticmethod
    def validate() -> bool:
        """Validate that required configuration is present."""
        if not Config.TOKEN:
            raise ValueError("DISCORD_TOKEN is not set in .env file")
        return True
