import os
from dotenv import load_dotenv
from dms.localization import t

load_dotenv()


class Config:
    """Bot configuration class."""

    _raw_db_url = os.getenv("DATABASE_URL")

    # Heroku provides postgres://, SQLAlchemy expects postgresql+psycopg2://
    if _raw_db_url and _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql+psycopg2://", 1)

    # Fallback URL for local development
    DATABASE_URL = _raw_db_url or "sqlite:///bot.db"

    # Discord bot token (required)
    TOKEN: str | None = os.getenv("DISCORD_TOKEN")

    # Command prefix
    PREFIX: str = os.getenv("COMMAND_PREFIX", "!")

    # Bot owner ID (optional)
    OWNER_ID: int | None = int(os.getenv("OWNER_ID")) if os.getenv("OWNER_ID") else None

    # Welcome/onboarding text used in DM greeting
    WELCOME_MESSAGE_ENG: str = os.getenv(
        "WELCOME_MESSAGE",
        t("en", "welcome_message_default"),
    )

    WELCOME_MESSAGE_RUS: str = os.getenv(
        "WELCOME_MESSAGE_RUS",
        t("ru", "welcome_message_default"),
    )

    # Discord channel ID used as fallback when a DM cannot be delivered
    FALLBACK_CHANNEL_ID: int = int(os.getenv("FALLBACK_CHANNEL_ID", "0"))

    # Default language for UI text shown outside user-specific context (e.g., role_panel)
    DEFAULT_LANG: str = os.getenv("DEFAULT_LANG", "ru")

    # Game role definitions shown in role selection panels; structure: id, label_en/label_ru, emoji
    GAME_ROLE_DEFINITIONS: list[dict] = [
        {
            "id": int(os.getenv("GAME_ROLE_ARMA3_ID", "0")),
            "label_en": t("en", "config_game_role_arma3_label"),
            "label_ru": t("ru", "config_game_role_arma3_label"),
            "description_en": t("en", "config_game_role_arma3_description"),
            "description_ru": t("ru", "config_game_role_arma3_description"),
            "emoji": "<:ARMA3:1444025332586905711>",
        },
        {
            "id": int(os.getenv("GAME_ROLE_SQUAD_ID", "0")),
            "label_en": t("en", "config_game_role_squad_label"),
            "label_ru": t("ru", "config_game_role_squad_label"),
            "description_en": t("en", "config_game_role_squad_description"),
            "description_ru": t("ru", "config_game_role_squad_description"),
            "emoji": "<:SQUAD:1444025248323207330>",
        },
        {
            "id": int(os.getenv("GAME_ROLE_CSGO_ID", "0")),
            "label_en": t("en", "config_game_role_csgo_label"),
            "label_ru": t("ru", "config_game_role_csgo_label"),
            "description_en": t("en", "config_game_role_csgo_description"),
            "description_ru": t("ru", "config_game_role_csgo_description"),
            "emoji": "<:CSGO:1444025289708666981>",
        },
        {
            "id": int(os.getenv("GAME_ROLE_MINECRAFT_ID", "0")),
            "label_en": t("en", "config_game_role_minecraft_label"),
            "label_ru": t("ru", "config_game_role_minecraft_label"),
            "description_en": t("en", "config_game_role_minecraft_description"),
            "description_ru": t("ru", "config_game_role_minecraft_description"),
            "emoji": "<:MINECRAFT:1444025385754034377>",
        },
        {
            "id": int(os.getenv("GAME_ROLE_RUST_ID", "0")),
            "label_en": t("en", "config_game_role_rust_label"),
            "label_ru": t("ru", "config_game_role_rust_label"),
            "description_en": t("en", "config_game_role_rust_description"),
            "description_ru": t("ru", "config_game_role_rust_description"),
            "emoji": "<:RUST:1444025421225267230>",
        },
        # Add/edit items above as needed: id, label_en/label_ru, emoji
    ]

    ARMA_ROLE_DEFINITIONS = [
        {
            "id": int(os.getenv("ARMA_ROLE_SQUAD_LEADER_ID", "0")),
            "label_en": t("en", "config_arma_role_squad_leader_label"),
            "label_ru": t("ru", "config_arma_role_squad_leader_label"),
            "description_en": t("en", "config_arma_role_squad_leader_description"),
            "description_ru": t("ru", "config_arma_role_squad_leader_description"),
            "emoji": "🗺️",
        },
        {
            "id": int(os.getenv("ARMA_ROLE_TEAM_LEADER_ID", "0")),
            "label_en": t("en", "config_arma_role_team_leader_label"),
            "label_ru": t("ru", "config_arma_role_team_leader_label"),
            "description_en": t("en", "config_arma_role_team_leader_description"),
            "description_ru": t("ru", "config_arma_role_team_leader_description"),
            "emoji": "📡",
        },
        {
            "id": int(os.getenv("ARMA_ROLE_RIFLEMAN_ID", "0")),
            "label_en": t("en", "config_arma_role_rifleman_label"),
            "label_ru": t("ru", "config_arma_role_rifleman_label"),
            "description_en": t("en", "config_arma_role_rifleman_description"),
            "description_ru": t("ru", "config_arma_role_rifleman_description"),
            "emoji": "🎯",
        },
        {
            "id": int(os.getenv("ARMA_ROLE_MEDIC_ID", "0")),
            "label_en": t("en", "config_arma_role_medic_label"),
            "label_ru": t("ru", "config_arma_role_medic_label"),
            "description_en": t("en", "config_arma_role_medic_description"),
            "description_ru": t("ru", "config_arma_role_medic_description"),
            "emoji": "🩺",
        },
        {
            "id": int(os.getenv("ARMA_ROLE_AUTORIFLEMAN_ID", "0")),
            "label_en": t("en", "config_arma_role_autorifleman_label"),
            "label_ru": t("ru", "config_arma_role_autorifleman_label"),
            "description_en": t("en", "config_arma_role_autorifleman_description"),
            "description_ru": t("ru", "config_arma_role_autorifleman_description"),
            "emoji": "💥",
        },
        {
            "id": int(os.getenv("ARMA_ROLE_AT_SPECIALIST_ID", "0")),
            "label_en": t("en", "config_arma_role_at_specialist_label"),
            "label_ru": t("ru", "config_arma_role_at_specialist_label"),
            "description_en": t("en", "config_arma_role_at_specialist_description"),
            "description_ru": t("ru", "config_arma_role_at_specialist_description"),
            "emoji": "🚀",
        },
        {
            "id": int(os.getenv("ARMA_ROLE_MARKSMAN_ID", "0")),
            "label_en": t("en", "config_arma_role_marksman_label"),
            "label_ru": t("ru", "config_arma_role_marksman_label"),
            "description_en": t("en", "config_arma_role_marksman_description"),
            "description_ru": t("ru", "config_arma_role_marksman_description"),
            "emoji": "🎯",
        },
        {
            "id": int(os.getenv("ARMA_ROLE_ENGINEER_ID", "0")),
            "label_en": t("en", "config_arma_role_engineer_label"),
            "label_ru": t("ru", "config_arma_role_engineer_label"),
            "description_en": t("en", "config_arma_role_engineer_description"),
            "description_ru": t("ru", "config_arma_role_engineer_description"),
            "emoji": "🔧",
        },
    ]

    # Recruit role ID (button "Register as Recruit")
    RECRUIT_ROLE_ID: int = int(os.getenv("RECRUIT_ROLE_ID", "0"))

    # Static list of roles that can be self-assigned via onboarding DM
    ROLE_DEFINITIONS_ENG: list[dict] = [
        {
            "label": t("en", "role_def_assault_label"),
            "description": t("en", "role_def_assault_description"),
            "id": int(os.getenv("ROLE_ASSAULT_ID", "0")),
        },
        {
            "label": t("en", "role_def_medic_label"),
            "description": t("en", "role_def_medic_description"),
            "id": int(os.getenv("ROLE_MEDIC_ID", "0")),
        },
        {
            "label": t("en", "role_def_pilot_label"),
            "description": t("en", "role_def_pilot_description"),
            "id": int(os.getenv("ROLE_PILOT_ID", "0")),
        },
        {
            "label": t("en", "role_def_support_label"),
            "description": t("en", "role_def_support_description"),
            "id": int(os.getenv("ROLE_SUPPORT_ID", "0")),
        },
    ]

    ROLE_DEFINITIONS_RUS: list[dict] = [
        {
            "label": t("ru", "role_def_assault_label"),
            "description": t("ru", "role_def_assault_description"),
            "id": int(os.getenv("ROLE_ASSAULT_ID", "0")),
        },
        {
            "label": t("ru", "role_def_medic_label"),
            "description": t("ru", "role_def_medic_description"),
            "id": int(os.getenv("ROLE_MEDIC_ID", "0")),
        },
        {
            "label": t("ru", "role_def_pilot_label"),
            "description": t("ru", "role_def_pilot_description"),
            "id": int(os.getenv("ROLE_PILOT_ID", "0")),
        },
        {
            "label": t("ru", "role_def_support_label"),
            "description": t("ru", "role_def_support_description"),
            "id": int(os.getenv("ROLE_SUPPORT_ID", "0")),
        },
    ]

    RECRUITER_ROLE_ID: int = int(os.getenv("RECRUITER_ROLE_ID") or "0")
    RECRUIT_CATEGORY_ID: int = int(os.getenv("RECRUIT_CATEGORY_ID") or "0")

    # Member role that is granted after recruit approval
    MEMBER_ROLE_ID: int = int(os.getenv("MEMBER_ROLE_ID", "0"))

    # Category used to store archived recruit channels (0 disables archiving)
    RECRUIT_ARCHIVE_CATEGORY_ID: int = int(os.getenv("RECRUIT_ARCHIVE_CATEGORY_ID", "0"))

    @staticmethod
    def validate() -> bool:
        """Validate that required configuration is present."""
        lang = getattr(Config, "DEFAULT_LANG", "en")
        if not Config.TOKEN:
            raise ValueError(t(lang, "missing_discord_token_env"))
        return True
