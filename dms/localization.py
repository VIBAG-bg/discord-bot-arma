# dms/localization.py

LANGS = {
    "en": {
        "greeting": "Hello, {name}!",
        "roles_header": "Available server roles:",
        "roles_hint": "Press role buttons below to assign them instantly.",
        "bot_description": "ARMA 3 Community Discord Bot",
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
        "language_name_en": "English",
        "language_name_ru": "Russian",
        "language_name_uk": "Ukrainian",
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
        "role_default_label": "Role",
        "role_with_description": "{mention} - {desc}",
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
        "recruit_channels_error": (
            "Recruit role assigned, but interview channels could not be created. "
            "Please contact staff."
        ),
        "recruit_channels_existing": (
            'Recruit role "{role}" assigned!\n'
            "Your application status: **READY**.\n\n"
            "Your interview channels already exist:\n"
            "- Text: {text}\n"
            "- Voice: {voice}"
        ),
        "recruit_channels_created": (
            'Recruit role "{role}" assigned!\n'
            "Your application status: **READY**.\n\n"
            "A private interview text & voice channel have been created for you:\n"
            "- Text: {text}\n"
            "- Voice: {voice}"
        ),
        "recruit_embed_title": "Recruit {name} ready for interview",
        "recruit_embed_status_ready": "READY FOR INTERVIEW",
        "recruit_embed_field_code": "Recruit code",
        "recruit_embed_field_discord": "Discord",
        "recruit_embed_field_steam": "Steam",
        "recruit_embed_steam_not_linked": "Not linked",
        "recruit_embed_steam_not_linked_bilingual": "Not linked / Не привязан",
        "recruit_embed_field_language": "Language",
        "recruit_embed_field_status": "Status",
        "recruit_embed_footer_interview": "Use this channel to schedule and run the interview.",
        "recruit_info_title": "Recruit info",
        "recruit_field_text_channel": "Text channel",
        "recruit_field_voice_channel": "Voice channel",
        "value_unknown": "Unknown",
        "recruits_unknown_status": "Unknown status. Use: pending / ready / done / rejected.",
        "recruits_none_with_status": "No recruits with status **{status}**.",
        "recruits_with_status_title": "Recruits with status {status}",
        "recruits_overview_title": "Recruits overview",
        "recruits_overview_none": "_none_",
        "user_not_in_guild": "User is not a member of this guild.",
        "user_synced": (
            "User `{target}` synced.\n"
            "discord_id={discord_id}, username=`{username}`, "
            "display_name=`{display_name}`, is_admin={is_admin}"
        ),
        "command_guild_only": "This command can only be used in a guild.",
        "user_updates_done": "Updated {updated} users from guild `{guild}`.",
        "command_not_found": "Command not found. Use `{prefix}help` to see available commands.",
        "missing_permissions": "You do not have permission to use this command.",
        "missing_required_argument": "Missing required argument: {param}",
        "bad_argument": "Bad argument: {error}",
        "command_on_cooldown": "This command is on cooldown. Try again in {retry_after:.2f}s",
        "error_generic": "An error occurred while executing the command.",
        "help_title": "Справка • ARMA 3 Bot",
        "help_description": (
            "Available commands by category.\n"
            "Use `{prefix}help <command>` to see details."
        ),
        "help_admin_commands": "🔒 Команды администраторов",
        "help_general_category": "General",
        "help_command_line": "`{signature}` — {description}",
        "help_command_title": "Command: {signature}",
        "help_category_title": "Category: {name}",
        "no_description": "No description.",
        "help_desc_ping": "Check the bot's latency.",
        "help_desc_info": "Show information about the bot.",
        "help_desc_serverinfo": "Show information about the current server.",
        "help_desc_userinfo": "Show information about a user.",
        "help_desc_avatar": "Show a user's avatar.",
        "help_desc_say": "Send a message (optionally as an embed) to a channel.",
        "help_desc_onboarding": "Resend onboarding DM to yourself.",
        "help_desc_onboarding_for": "Send onboarding DM to a specific member.",
        "help_desc_recruit": "Show recruit profile details.",
        "help_desc_recruits": "List recruits, optionally filtered by status.",
        "help_desc_user_update": "Synchronize a user's profile from Discord.",
        "help_desc_user_updates": "Bulk synchronize all non-bot members.",
        "help_desc_role_panel": "Post the roles selection panel with buttons.",
        "help_desc_kick": "Kick a member from the server.",
        "help_desc_ban": "Ban a member from the server.",
        "help_desc_unban": "Unban a user by ID.",
        "help_desc_clear": "Delete multiple recent messages.",
        "help_desc_mute": "Timeout (mute) a member for a duration.",
        "help_desc_unmute": "Remove timeout from a member.",
        "steam_modal_title": "Link your Steam ID",
        "steam_modal_label": "Your Steam ID / SteamID64",
        "steam_modal_placeholder": "Example: 7656119XXXXXXXXXX",
        "steam_modal_wrong_user": "This form is bound to another user.",
        "steam_modal_error": "Internal error while saving Steam ID. Contact staff.",
        "btn_yes": "Yes",
        "btn_no": "No",
        "btn_approve": "Approve",
        "btn_deny": "Deny",
        "mod_cannot_target_self_kick": "🚫 You cannot kick yourself!",
        "mod_cannot_target_self_ban": "🚫 You cannot ban yourself!",
        "mod_cannot_target_self_mute": "🚫 You cannot mute yourself!",
        "mod_cannot_target_higher": "🚫 You cannot target someone with a higher or equal role!",
        "mod_bot_cannot_target_higher": "🚫 I cannot target someone with a higher or equal role than me!",
        "mod_kick_title": "🔨 Member Kicked",
        "mod_kick_description": "{member} has been kicked from the server.",
        "mod_ban_title": "⛔ Member Banned",
        "mod_ban_description": "{member} has been banned from the server.",
        "mod_unban_title": "✅ User Unbanned",
        "mod_unban_description": "{user} ({name}) has been unbanned.",
        "mod_mute_title": "🔇 Member Muted",
        "mod_mute_description": "{member} has been muted.",
        "mod_unmute_title": "🔈 Member Unmuted",
        "mod_unmute_description": "{member} has been unmuted.",
        "mod_reason": "Reason",
        "mod_moderator": "Moderator",
        "mod_user_id": "User ID: {user_id}",
        "mod_no_permission_kick": "🚫 I don't have permission to kick this member.",
        "mod_no_permission_ban": "🚫 I don't have permission to ban this member.",
        "mod_no_permission_unban": "🚫 I don't have permission to unban users.",
        "mod_no_permission_clear": "🚫 I don't have permission to delete messages.",
        "mod_no_permission_mute": "🚫 I don't have permission to timeout this member.",
        "mod_clear_amount_min": "🚫 Amount must be at least 1.",
        "mod_clear_amount_max": "🚫 Amount cannot exceed 100 messages.",
        "mod_clear_deleted": "🧹 Deleted {count} message(s).",
        "mod_mute_duration_invalid": "🚫 Duration must be between 1 and 40320 minutes (28 days).",
        "mod_duration": "Duration",
        "mod_duration_minutes": "{minutes} minutes",
        "mod_error_generic": "🚫 An error occurred: {error}",
        "mod_user_not_found_or_not_banned": "🚫 User not found or not banned.",
        "recruit_category_not_configured": "Recruit category is not configured correctly.",
        "recruit_not_found_server": "Recruit not found on the server.",
        "recruit_moderation_missing_steam": (
            "This recruit has not linked their **SteamID64** yet.\n\n"
            "Ask them to open their DMs with the bot and press the "
            "**\"Link Steam ID\"** button in the onboarding message.\n"
            "After that you can approve the application."
        ),
        "recruit_moderation_dm_link_steam": (
            "To complete your recruit application, please link your **SteamID64**.\n"
            "Press the **\"Link Steam ID\"** button below and submit your 17-digit SteamID64."
        ),
        "recruit_moderation_dm_approved": (
            "Congratulations! Your recruit application has been approved. "
            "Now you are a full member and got your member role! Welcome aboard!"
        ),
        "recruit_moderation_dm_rejected": (
            "Unfortunately, your recruit application has been rejected."
        ),
        "recruit_moderation_approved_followup": "Recruit approved, channels archived.",
        "recruit_moderation_rejected_followup": "Recruit denied, channels archived.",
        "recruit_moderation_approved_channel": "Recruit {recruit} approved by {moderator}.",
        "recruit_moderation_rejected_channel": "Recruit {recruit} rejected by {moderator}.",
        "recruit_moderation_confirm_approve": "Are you sure you want to **APPROVE** {recruit}?",
        "recruit_moderation_confirm_deny": "Are you sure you want to **DENY** {recruit}?",
        "recruit_moderation_not_allowed_approve": "You are not allowed to approve recruits.",
        "recruit_moderation_not_allowed_deny": "You are not allowed to deny recruits.",
        "recruit_moderation_confirm_yes": "Approved.",
        "recruit_moderation_confirm_no": "Cancelled.",
        "recruit_moderation_denied_label": "Denied.",
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
        "notify_dm_disabled": (
            "{member}, enable direct messages so I can send your onboarding instructions. "
            "After this, please send the `{command}` command on the server."
        ),
        "presence_help_hint": "{prefix}help | ARMA 3",
        "member_left_server": "{name} has left the server.",
        "recruit_auto_granted": (
            "You have been granted the **Recruit** role by staff.\n\n"
            "To complete your registration, please link your SteamID64.\n"
            "Press the button below and fill in the form."
        ),
        "welcome_message_default": (
            "Welcome to the ARMA 3 tactical community. We focus on coordination, discipline, "
            "and joint operations. Before we deploy, please choose your roles and register as a "
            "recruit so the staff can learn your interests and prepare you for upcoming missions."
        ),
        "config_game_role_arma3_label": "ARMA 3",
        "config_game_role_arma3_description": "Tactical military simulation game.",
        "config_game_role_squad_label": "Squad",
        "config_game_role_squad_description": "Team-based military FPS game.",
        "config_game_role_csgo_label": "CS GO",
        "config_game_role_csgo_description": "Competitive first-person shooter game.",
        "config_game_role_minecraft_label": "Minecraft",
        "config_game_role_minecraft_description": "Sandbox construction and survival game.",
        "config_game_role_rust_label": "Rust",
        "config_game_role_rust_description": "Survival game set in a post-apocalyptic world.",
        "config_arma_role_squad_leader_label": "Squad Leader",
        "config_arma_role_squad_leader_description": (
            "Leads the squad, coordinates movement and communication."
        ),
        "config_arma_role_team_leader_label": "Team Leader",
        "config_arma_role_team_leader_description": "Leads a fireteam during engagements.",
        "config_arma_role_rifleman_label": "Rifleman",
        "config_arma_role_rifleman_description": (
            "Standard infantry role, main firepower of the squad."
        ),
        "config_arma_role_medic_label": "Medic",
        "config_arma_role_medic_description": (
            "Provides medical support and stabilizes injured teammates."
        ),
        "config_arma_role_autorifleman_label": "Autorifleman",
        "config_arma_role_autorifleman_description": (
            "Delivers suppressive fire using a machine gun."
        ),
        "config_arma_role_at_specialist_label": "AT Specialist",
        "config_arma_role_at_specialist_description": (
            "Carries anti-tank weapons and engages armored vehicles."
        ),
        "config_arma_role_marksman_label": "Marksman",
        "config_arma_role_marksman_description": (
            "Engages targets at medium-long distances with high accuracy."
        ),
        "config_arma_role_engineer_label": "Engineer",
        "config_arma_role_engineer_description": (
            "Handles explosives, repairs vehicles, performs technical tasks."
        ),
        "role_def_assault_label": "Assault",
        "role_def_assault_description": "Frontline infantry focused on direct engagements.",
        "role_def_medic_label": "Medic",
        "role_def_medic_description": "Keeps squads alive with triage and evacuations.",
        "role_def_pilot_label": "Pilot",
        "role_def_pilot_description": (
            "Provides air transport, close air support, and logistics."
        ),
        "role_def_support_label": "Support",
        "role_def_support_description": "Handles vehicles, heavy weapons, and resupply.",
        "missing_discord_token_env": "DISCORD_TOKEN is not set in .env file",
    },
    "ru": {
        "greeting": "Привет, {name}!",
        "roles_header": "Доступные роли на сервере:",
        "roles_hint": "Нажмите на кнопки ролей ниже, чтобы выдать их себе.",
        "bot_description": "Discord-бот сообщества ARMA 3",
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
        "language_name_en": "Английский",
        "language_name_ru": "Русский",
        "language_name_uk": "Украинский",
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
        "role_default_label": "Роль",
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
        "recruit_channels_error": (
            "Роль рекрута выдана, но не удалось создать каналы для собеседования. "
            "Свяжитесь с персоналом."
        ),
        "recruit_channels_existing": (
            "Роль рекрута \"{role}\" выдана!\n"
            "Статус заявки: **READY**.\n\n"
            "Каналы для собеседования уже существуют:\n"
            "- Текст: {text}\n"
            "- Голос: {voice}"
        ),
        "recruit_channels_created": (
            "Роль рекрута \"{role}\" выдана!\n"
            "Статус заявки: **READY**.\n\n"
            "Для вас созданы приватные текстовый и голосовой каналы:\n"
            "- Текст: {text}\n"
            "- Голос: {voice}"
        ),
        "recruit_embed_title": "Рекрут {name} готов к собеседованию",
        "recruit_embed_status_ready": "READY FOR INTERVIEW",
        "recruit_embed_field_code": "Код рекрута",
        "recruit_embed_field_discord": "Discord",
        "recruit_embed_field_steam": "Steam",
        "recruit_embed_steam_not_linked": "Не привязан",
        "recruit_embed_field_language": "Язык",
        "recruit_embed_field_status": "Статус",
        "recruit_embed_footer_interview": "Используйте этот канал, чтобы назначить и провести собеседование.",
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
        "notify_dm_disabled": (
            "{member}, включите личные сообщения, чтобы я мог отправить инструкции по онбордингу. "
            "После этого отправьте команду `{command}` на сервере."
        ),
        "presence_help_hint": "{prefix}help | ARMA 3",
        "member_left_server": "{name} покинул сервер.",
        "recruit_auto_granted": (
            "Вам выдали роль **Recruit**.\n\n"
            "Чтобы завершить регистрацию, привяжите ваш SteamID64.\n"
            "Нажмите кнопку ниже и заполните форму."
        ),
        "recruit_info_title": "Информация о рекруте",
        "recruit_field_text_channel": "Текстовый канал",
        "recruit_field_voice_channel": "Голосовой канал",
        "value_unknown": "Неизвестно",
        "recruits_unknown_status": "Неизвестный статус. Используйте: pending / ready / done / rejected.",
        "recruits_none_with_status": "Нет рекрутов со статусом **{status}**.",
        "recruits_with_status_title": "Рекруты со статусом {status}",
        "recruits_overview_title": "Сводка по рекрутам",
        "recruits_overview_none": "_нет_",
        "user_not_in_guild": "Пользователь не является участником этого сервера.",
        "user_synced": (
            "Пользователь `{target}` синхронизирован.\n"
            "discord_id={discord_id}, username=`{username}`, "
            "display_name=`{display_name}`, is_admin={is_admin}"
        ),
        "command_guild_only": "Эту команду можно использовать только на сервере.",
        "user_updates_done": "Обновлено {updated} пользователей из сервера `{guild}`.",
        "command_not_found": "Команда не найдена. Используйте `{prefix}help`, чтобы увидеть список команд.",
        "missing_permissions": "У вас нет прав использовать эту команду.",
        "missing_required_argument": "Отсутствует обязательный аргумент: {param}",
        "bad_argument": "Некорректный аргумент: {error}",
        "command_on_cooldown": "Эта команда на кулдауне. Попробуйте через {retry_after:.2f} сек.",
        "error_generic": "Произошла ошибка при выполнении команды.",
        "help_title": "Справка • ARMA 3 Bot",
        "help_description": (
            "Доступные команды по категориям.\n"
            "Используйте `{prefix}help <command>`, чтобы увидеть подробности."
        ),
        "help_admin_commands": "🔒 Команды администраторов",
        "help_general_category": "Общие",
        "help_command_line": "`{signature}` — {description}",
        "help_command_title": "Команда: {signature}",
        "help_category_title": "Категория: {name}",
        "no_description": "Описание отсутствует.",
        "help_desc_ping": "Проверить задержку бота.",
        "help_desc_info": "Показать информацию о боте.",
        "help_desc_serverinfo": "Показать информацию о текущем сервере.",
        "help_desc_userinfo": "Показать информацию о пользователе.",
        "help_desc_avatar": "Показать аватар пользователя.",
        "help_desc_say": "Отправить сообщение (при желании в embed) в канал.",
        "help_desc_onboarding": "Выслать онбординг-сообщение себе в личку.",
        "help_desc_onboarding_for": "Отправить онбординг-сообщение выбранному участнику.",
        "help_desc_recruit": "Показать данные анкеты рекрута.",
        "help_desc_recruits": "Список рекрутов с необязательным фильтром по статусу.",
        "help_desc_user_update": "Синхронизировать профиль пользователя из Discord.",
        "help_desc_user_updates": "Массово синхронизировать всех участников (кроме ботов).",
        "help_desc_role_panel": "Опубликовать панель выбора ролей с кнопками.",
        "help_desc_kick": "Кикнуть участника с сервера.",
        "help_desc_ban": "Забанить участника на сервере.",
        "help_desc_unban": "Разбанить пользователя по ID.",
        "help_desc_clear": "Удалить несколько последних сообщений.",
        "help_desc_mute": "Выдать тайм-аут (мьют) участнику на время.",
        "help_desc_unmute": "Снять тайм-аут с участника.",
        "steam_modal_title": "Привяжите Steam ID",
        "steam_modal_label": "Ваш Steam ID / SteamID64",
        "steam_modal_placeholder": "Пример: 7656119XXXXXXXXXX",
        "steam_modal_wrong_user": "Эта форма привязана к другому пользователю.",
        "steam_modal_error": "Внутренняя ошибка при сохранении Steam ID. Обратитесь к персоналу.",
        "btn_yes": "Да",
        "btn_no": "Нет",
        "btn_approve": "Одобрить",
        "btn_deny": "Отклонить",
        "mod_cannot_target_self_kick": "🚫 Нельзя кикнуть себя.",
        "mod_cannot_target_self_ban": "🚫 Нельзя забанить себя.",
        "mod_cannot_target_self_mute": "🚫 Нельзя замьютить себя.",
        "mod_cannot_target_higher": "🚫 Нельзя действовать на того, у кого выше или равная роль.",
        "mod_bot_cannot_target_higher": "🚫 Я не могу действовать на пользователя с ролью выше или равной моей.",
        "mod_kick_title": "🔨 Участник кикнут",
        "mod_kick_description": "{member} был кикнут с сервера.",
        "mod_ban_title": "⛔ Участник забанен",
        "mod_ban_description": "{member} был забанен на сервере.",
        "mod_unban_title": "✅ Пользователь разбанен",
        "mod_unban_description": "{user} ({name}) был разбанен.",
        "mod_mute_title": "🔇 Участник замьючен",
        "mod_mute_description": "{member} был замьючен.",
        "mod_unmute_title": "🔈 Участник размьючен",
        "mod_unmute_description": "{member} был размьючен.",
        "mod_reason": "Причина",
        "mod_moderator": "Модератор",
        "mod_user_id": "ID пользователя: {user_id}",
        "mod_no_permission_kick": "🚫 У меня нет прав кикать этого участника.",
        "mod_no_permission_ban": "🚫 У меня нет прав банить этого участника.",
        "mod_no_permission_unban": "🚫 У меня нет прав разбанивать пользователей.",
        "mod_no_permission_clear": "🚫 У меня нет прав удалять сообщения.",
        "mod_no_permission_mute": "🚫 У меня нет прав выдавать тайм-аут этому участнику.",
        "mod_clear_amount_min": "🚫 Количество должно быть не меньше 1.",
        "mod_clear_amount_max": "🚫 Количество не может превышать 100 сообщений.",
        "mod_clear_deleted": "🧹 Удалено {count} сообщений.",
        "mod_mute_duration_invalid": "🚫 Длительность должна быть от 1 до 40320 минут (28 дней).",
        "mod_duration": "Длительность",
        "mod_duration_minutes": "{minutes} минут",
        "mod_error_generic": "🚫 Произошла ошибка: {error}",
        "mod_user_not_found_or_not_banned": "🚫 Пользователь не найден или не забанен.",
        "role_with_description": "{mention} - {desc}",
        "recruit_category_not_configured": "Категория для рекрутов настроена некорректно.",
        "recruit_not_found_server": "Рекрут не найден на сервере.",
        "recruit_moderation_missing_steam": (
            "Этот рекрут ещё не привязал свой **SteamID64**.\n\n"
            "Попросите его открыть личные сообщения с ботом и нажать кнопку "
            "**\"Link Steam ID\"** в онбординг-сообщении.\n"
            "После этого можно одобрить заявку."
        ),
        "recruit_moderation_dm_link_steam": (
            "Чтобы завершить заявку рекрута, привяжите свой **SteamID64**.\n"
            "Нажмите кнопку **\"Link Steam ID\"** ниже и отправьте свой 17-значный SteamID64."
        ),
        "recruit_moderation_dm_approved": (
            "Поздравляем! Ваша заявка рекрута одобрена. "
            "Теперь вы полноценный участник и получили роль участника! Добро пожаловать!"
        ),
        "recruit_moderation_dm_rejected": (
            "К сожалению, ваша заявка рекрута отклонена."
        ),
        "recruit_moderation_approved_followup": "Рекрут одобрен, каналы архивированы.",
        "recruit_moderation_rejected_followup": "Рекрут отклонён, каналы архивированы.",
        "recruit_moderation_approved_channel": "Рекрут {recruit} одобрен {moderator}.",
        "recruit_moderation_rejected_channel": "Рекрут {recruit} отклонён {moderator}.",
        "recruit_moderation_confirm_approve": "Вы уверены, что хотите **ОДОБРИТЬ** {recruit}?",
        "recruit_moderation_confirm_deny": "Вы уверены, что хотите **ОТКЛОНИТЬ** {recruit}?",
        "recruit_moderation_not_allowed_approve": "У вас нет права одобрять рекрутов.",
        "recruit_moderation_not_allowed_deny": "У вас нет права отклонять рекрутов.",
        "recruit_moderation_confirm_yes": "Одобрено.",
        "recruit_moderation_confirm_no": "Отменено.",
        "recruit_moderation_denied_label": "Отклонено.",
        "recruit_embed_steam_not_linked_bilingual": "Не привязан / Not linked",

        "welcome_message_default": (
            "Добро пожаловать в тактическое сообщество ARMA 3. Мы уделяем внимание "
            "координации, дисциплине и совместным операциям. Перед тем как начать, "
            "выберите роли и зарегистрируйтесь как рекрут, чтобы рекрутеры могли узнать ваши "
            "интересы и подготовить вас к предстоящим миссиям."
        ),
        "config_game_role_arma3_label": "ARMA 3",
        "config_game_role_arma3_description": "Тактический военный симулятор.",
        "config_game_role_squad_label": "Squad",
        "config_game_role_squad_description": "Командный военный шутер от первого лица.",
        "config_game_role_csgo_label": "CS GO",
        "config_game_role_csgo_description": "Соревновательный шутер от первого лица.",
        "config_game_role_minecraft_label": "Minecraft",
        "config_game_role_minecraft_description": "Песочница про строительство и выживание.",
        "config_game_role_rust_label": "Rust",
        "config_game_role_rust_description": "Выживание в постапокалиптическом мире.",
        "config_arma_role_squad_leader_label": "Командир отделения",
        "config_arma_role_squad_leader_description": (
            "Ведет отделение, координирует перемещения и связь."
        ),
        "config_arma_role_team_leader_label": "Командир звена",
        "config_arma_role_team_leader_description": (
            "Командует звеном во время боевого контакта."
        ),
        "config_arma_role_rifleman_label": "Стрелок",
        "config_arma_role_rifleman_description": (
            "Базовая стрелковая роль, основной огневой ресурс отделения."
        ),
        "config_arma_role_medic_label": "Медик",
        "config_arma_role_medic_description": (
            "Оказывает медицинскую поддержку и стабилизирует раненых."
        ),
        "config_arma_role_autorifleman_label": "Пулеметчик",
        "config_arma_role_autorifleman_description": (
            "Ведет подавляющий огонь из пулемета."
        ),
        "config_arma_role_at_specialist_label": "ПТ-специалист",
        "config_arma_role_at_specialist_description": (
            "Использует противотанковое оружие и поражает бронетехнику."
        ),
        "config_arma_role_marksman_label": "Маркер / Дальний стрелок",
        "config_arma_role_marksman_description": (
            "Поражает цели на средних и дальних дистанциях с высокой точностью."
        ),
        "config_arma_role_engineer_label": "Инженер",
        "config_arma_role_engineer_description": (
            "Работает со взрывчаткой, ремонтирует технику, решает технические задачи."
        ),
        "role_def_assault_label": "Штурм",
        "role_def_assault_description": (
            "Линейная пехота, сфокусированная на прямых столкновениях."
        ),
        "role_def_medic_label": "Медик",
        "role_def_medic_description": (
            "Поддерживает отделения за счет медицины и эвакуации."
        ),
        "role_def_pilot_label": "Пилот",
        "role_def_pilot_description": (
            "Обеспечивает воздушный транспорт, поддержку с воздуха и логистику."
        ),
        "role_def_support_label": "Поддержка",
        "role_def_support_description": (
            "Работает с техникой, тяжелым вооружением и снабжением."
        ),
        "missing_discord_token_env": "DISCORD_TOKEN не указан в файле .env",
    },
    "uk": {
        "greeting": "Привіт, {name}!",
        "roles_header": "Доступні ролі на сервері:",
        "roles_hint": "Натисніть на кнопки ролей нижче, щоб видати їх собі.",
        "bot_description": "Discord-бот спільноти ARMA 3",
        "recruit_hint": (
            "Щоб зареєструватися рекрутом ARMA 3:\n"
            "→ Натисніть зелену кнопку «Register as Recruit»."
        ),
        "steam_intro": (
            "Щоб завершити онбординг, прив’яжіть ваш Steam-акаунт.\n\n"
            "Як знайти SteamID64:\n"
            "1) Відкрийте Steam і перейдіть на сторінку профілю.\n"
            "2) Натисніть ПКМ по сторінці → «Копіювати URL-адресу».\n"
            "3) Наприкінці посилання буде довге число — це ваш SteamID64.\n\n"
            "Натисніть кнопку **Link Steam ID** нижче та вставте це число у форму."
        ),
        "language_set": "Мову встановлено: UA",
        "choose_language": "Оберіть мову:",
        "language_name_en": "Англійська",
        "language_name_ru": "Російська",
        "language_name_uk": "Українська",
        "onboarding_guild_only": "Цю команду потрібно використовувати в каналі сервера, а не у приватних повідомленнях.",
        "onboarding_dm_sent_self": "Онбординг-повідомлення надіслано вам у приват.",
        "onboarding_dm_failed_self": (
            "Не вдалося надіслати вам приватне повідомлення. Увімкніть ДМ від учасників сервера та спробуйте знову."
        ),
        "onboarding_dm_sent_other": "Онбординг-повідомлення надіслано {member}.",
        "onboarding_dm_failed_other": "Не вдалося написати {member} у приват. Їхні ДМ, можливо, вимкнені.",
        "steam_link": (
            "⚠️ Перед тим як подати заявку рекрута, потрібно прив’язати Steam ID.\n\n"
            "Скористайся кнопкою нижче й введи свій 17-значний SteamID64."
        ),
        "invalid_steam_link": (
            "Це не схоже на коректний SteamID64.\n"
            "Відкрийте свій профіль у Steam → натисніть ПКМ по сторінці профілю → "
            "«Копіювати URL-адресу» → візьміть довге число в кінці."
        ),
        "steam_saved": "Steam ID **{steam_id}** збережено. Дякуємо!",
        "ping_title": "Понг!",
        "ping_description": "Затримка бота: **{latency} мс**",
        "role_default_label": "Роль",
        "info_title": "Інформація про бота",
        "info_description": "Discord-бот спільноти ARMA 3",
        "info_field_bot": "Бот",
        "info_field_servers": "Сервери",
        "info_field_users": "Користувачі",
        "info_field_uptime": "Час роботи",
        "info_uptime_value": "{hours}г {minutes}хв {seconds}с",
        "info_field_python_version": "Версія Python",
        "info_field_discordpy_version": "Версія discord.py",
        "requested_by": "Запрошено користувачем {requester}",
        "serverinfo_title": "Інформація про сервер: {name}",
        "serverinfo_owner": "Власник",
        "serverinfo_members": "Учасники",
        "serverinfo_channels": "Канали",
        "serverinfo_channels_value": "Текст: {text} | Голос: {voice}",
        "serverinfo_roles": "Ролі",
        "serverinfo_id": "ID сервера",
        "serverinfo_created_at": "Створено",
        "unknown_value": "Невідомо",
        "userinfo_title": "Інформація про користувача",
        "userinfo_name": "Ім’я",
        "userinfo_nickname": "Нікнейм",
        "userinfo_no_nickname": "Відсутній",
        "userinfo_id": "ID користувача",
        "userinfo_status": "Статус",
        "userinfo_joined": "Приєднався до сервера",
        "userinfo_created": "Аккаунт створено",
        "userinfo_roles_title": "Ролі [{count}]",
        "roles_count_only": "{count} ролей",
        "avatar_title": "Аватар користувача {name}",
        "avatar_download_links": "Посилання для завантаження",
        "avatar_download_links_value": "[PNG]({png}) | [JPG]({jpg}) | [WEBP]({webp})",
        "avatar_no_custom": "У цього користувача немає власного аватара.",
        "say_nothing_to_send": "Немає тексту для надсилання.",
        "recruit_channels_error": (
            "Роль рекрута видана, але не вдалося створити канали для співбесіди. "
            "Зв’яжіться з персоналом."
        ),
        "recruit_channels_existing": (
            'Роль рекрута "{role}" видана!\n'
            "Статус заявки: **READY**.\n\n"
            "Канали для співбесіди вже існують:\n"
            "- Текст: {text}\n"
            "- Голос: {voice}"
        ),
        "recruit_channels_created": (
            'Роль рекрута "{role}" видана!\n'
            "Статус заявки: **READY**.\n\n"
            "Для вас створено приватні текстовий і голосовий канали:\n"
            "- Текст: {text}\n"
            "- Голос: {voice}"
        ),
        "recruit_embed_title": "Рекрут {name} готовий до співбесіди",
        "recruit_embed_status_ready": "READY FOR INTERVIEW",
        "recruit_embed_field_code": "Код рекрута",
        "recruit_embed_field_discord": "Discord",
        "recruit_embed_field_steam": "Steam",
        "recruit_embed_steam_not_linked": "Не прив’язано",
        "recruit_embed_steam_not_linked_bilingual": "Не прив’язано / Not linked",
        "recruit_embed_field_language": "Мова",
        "recruit_embed_field_status": "Статус",
        "recruit_embed_footer_interview": "Використовуйте цей канал, щоб призначити й провести співбесіду.",
        "recruit_info_title": "Інформація про рекрута",
        "recruit_field_text_channel": "Текстовий канал",
        "recruit_field_voice_channel": "Голосовий канал",
        "value_unknown": "Невідомо",
        "recruits_unknown_status": "Невідомий статус. Використовуйте: pending / ready / done / rejected.",
        "recruits_none_with_status": "Немає рекрутів зі статусом **{status}**.",
        "recruits_with_status_title": "Рекрути зі статусом {status}",
        "recruits_overview_title": "Зведення по рекрутах",
        "recruits_overview_none": "_немає_",
        "user_not_in_guild": "Користувач не є учасником цього сервера.",
        "user_synced": (
            "Користувача `{target}` синхронізовано.\n"
            "discord_id={discord_id}, username=`{username}`, "
            "display_name=`{display_name}`, is_admin={is_admin}"
        ),
        "command_guild_only": "Цю команду можна використовувати лише на сервері.",
        "user_updates_done": "Оновлено {updated} користувачів із сервера `{guild}`.",
        "command_not_found": "Команда не знайдена. Використайте `{prefix}help`, щоб побачити доступні команди.",
        "missing_permissions": "У вас немає прав використовувати цю команду.",
        "missing_required_argument": "Відсутній обов’язковий аргумент: {param}",
        "bad_argument": "Некоректний аргумент: {error}",
        "command_on_cooldown": "Ця команда на кулдауні. Спробуйте через {retry_after:.2f} сек.",
        "error_generic": "Сталася помилка під час виконання команди.",
        "help_title": "Довідка • ARMA 3 Bot",
        "help_description": (
            "Доступні команди за категоріями.\n"
            "Використайте `{prefix}help <command>`, щоб побачити подробиці."
        ),
        "help_admin_commands": "🔒 Команди адміністраторів",
        "help_general_category": "Загальні",
        "help_command_line": "`{signature}` — {description}",
        "help_command_title": "Команда: {signature}",
        "help_category_title": "Категорія: {name}",
        "no_description": "Опис відсутній.",
        "help_desc_ping": "Перевірити затримку бота.",
        "help_desc_info": "Показати інформацію про бота.",
        "help_desc_serverinfo": "Показати інформацію про поточний сервер.",
        "help_desc_userinfo": "Показати інформацію про користувача.",
        "help_desc_avatar": "Показати аватар користувача.",
        "help_desc_say": "Надіслати повідомлення (за бажанням в embed) у канал.",
        "help_desc_onboarding": "Надіслати онбординг-повідомлення собі у приват.",
        "help_desc_onboarding_for": "Надіслати онбординг-повідомлення вибраному учаснику.",
        "help_desc_recruit": "Показати дані анкети рекрута.",
        "help_desc_recruits": "Список рекрутів із необов’язковим фільтром за статусом.",
        "help_desc_user_update": "Синхронізувати профіль користувача з Discord.",
        "help_desc_user_updates": "Масово синхронізувати всіх учасників (крім ботів).",
        "help_desc_role_panel": "Опублікувати панель вибору ролей із кнопками.",
        "help_desc_kick": "Кікнути учасника з сервера.",
        "help_desc_ban": "Забанити учасника на сервері.",
        "help_desc_unban": "Розбанити користувача за ID.",
        "help_desc_clear": "Видалити кілька останніх повідомлень.",
        "help_desc_mute": "Видати тайм-аут (м’ют) учаснику на час.",
        "help_desc_unmute": "Зняти тайм-аут з учасника.",
        "mod_cannot_target_self_kick": "🚫 Не можна кікнути себе.",
        "mod_cannot_target_self_ban": "🚫 Не можна забанити себе.",
        "mod_cannot_target_self_mute": "🚫 Не можна зам’ютити себе.",
        "mod_cannot_target_higher": "🚫 Не можна діяти на того, хто має вищу або рівну роль.",
        "mod_bot_cannot_target_higher": "🚫 Я не можу діяти на користувача з роллю вищою або рівною моїй.",
        "mod_kick_title": "🔨 Учасника кікнуто",
        "mod_kick_description": "{member} було кікнуто з сервера.",
        "mod_ban_title": "⛔ Учасника забанено",
        "mod_ban_description": "{member} було забанено на сервері.",
        "mod_unban_title": "✅ Користувача розбанено",
        "mod_unban_description": "{user} ({name}) було розбанено.",
        "mod_mute_title": "🔇 Учасника зам’ючено",
        "mod_mute_description": "{member} було зам’ючено.",
        "mod_unmute_title": "🔈 Учасника розм’ючено",
        "mod_unmute_description": "{member} було розм’ючено.",
        "mod_reason": "Причина",
        "mod_moderator": "Модератор",
        "mod_user_id": "ID користувача: {user_id}",
        "mod_no_permission_kick": "🚫 У мене немає прав кікати цього учасника.",
        "mod_no_permission_ban": "🚫 У мене немає прав банити цього учасника.",
        "mod_no_permission_unban": "🚫 У мене немає прав розбанювати користувачів.",
        "mod_no_permission_clear": "🚫 У мене немає прав видаляти повідомлення.",
        "mod_no_permission_mute": "🚫 У мене немає прав видавати тайм-аут цьому учаснику.",
        "mod_clear_amount_min": "🚫 Кількість має бути не менше 1.",
        "mod_clear_amount_max": "🚫 Кількість не може перевищувати 100 повідомлень.",
        "mod_clear_deleted": "🧹 Видалено {count} повідомлень.",
        "mod_mute_duration_invalid": "🚫 Тривалість має бути від 1 до 40320 хвилин (28 днів).",
        "mod_duration": "Тривалість",
        "mod_duration_minutes": "{minutes} хвилин",
        "mod_error_generic": "🚫 Сталася помилка: {error}",
        "mod_user_not_found_or_not_banned": "🚫 Користувача не знайдено або не забанено.",
        "recruit_category_not_configured": "Категорію для рекрутів налаштовано некоректно.",
        "recruit_not_found_server": "Рекрут не знайдений на сервері.",
        "recruit_moderation_missing_steam": (
            "Цей рекрут ще не прив’язав свій **SteamID64**.\n\n"
            "Попросіть його відкрити приватні повідомлення з ботом і натиснути кнопку "
            "**\"Link Steam ID\"** в онбординг-повідомленні.\n"
            "Після цього можна схвалити заявку."
        ),
        "recruit_moderation_dm_link_steam": (
            "Щоб завершити заявку рекрута, прив’яжіть свій **SteamID64**.\n"
            "Натисніть кнопку **\"Link Steam ID\"** нижче та відправте свій 17-значний SteamID64."
        ),
        "recruit_moderation_dm_approved": (
            "Вітаємо! Вашу заявку рекрута схвалено. "
            "Тепер ви повноправний учасник і отримали роль учасника! Ласкаво просимо!"
        ),
        "recruit_moderation_dm_rejected": (
            "На жаль, вашу заявку рекрута відхилено."
        ),
        "recruit_moderation_approved_followup": "Рекрута схвалено, канали архівовано.",
        "recruit_moderation_rejected_followup": "Рекрута відхилено, канали архівовано.",
        "recruit_moderation_approved_channel": "Рекрут {recruit} схвалений {moderator}.",
        "recruit_moderation_rejected_channel": "Рекрут {recruit} відхилений {moderator}.",
        "recruit_moderation_confirm_approve": "Ви впевнені, що хочете **СХВАЛИТИ** {recruit}?",
        "recruit_moderation_confirm_deny": "Ви впевнені, що хочете **ВІДХИЛИТИ** {recruit}?",
        "recruit_moderation_not_allowed_approve": "У вас немає права схвалювати рекрутів.",
        "recruit_moderation_not_allowed_deny": "У вас немає права відхиляти рекрутів.",
        "recruit_moderation_confirm_yes": "Схвалено.",
        "recruit_moderation_confirm_no": "Скасовано.",
        "recruit_moderation_denied_label": "Відхилено.",
        "recruit_already_applied": (
            "Ти вже подав заявку як рекрут. "
            "Якщо щось не так, напиши рекрутерам або модераторам."
        ),
        "recruit_role_not_configured": (
            "ID ролі рекрута налаштовано некоректно. "
            "Повідом, будь ласка, адміністрації сервера."
        ),
        "recruit_role_not_found": (
            "Роль рекрута не знайдена на сервері. "
            "Повідом, будь ласка, адміністрації сервера."
        ),
        "recruit_already_has_role": "Ти вже зареєстрований як рекрут.",
        "recruit_cannot_grant_role": (
            "Я не можу видати роль рекрута. "
            "Схоже, не вистачає прав. Звернись до адміністрації."
        ),
        "game_role_not_found": "Налаштовану ігрову роль не знайдено на сервері.",
        "no_permission_manage_roles": "У мене немає прав керувати твоїми ролями.",

        # Новий онбординг
        "onboarding_title": "Ласкаво просимо до нашої тактичної спільноти ARMA 3",
        "onboarding_body": (
            "Ми робимо акцент на координації, дисципліні та спільних операціях.\n"
            "Використовуйте кнопки нижче, щоб налаштувати свій профіль:"
        ),
        "btn_games": "Ігрові ролі",
        "btn_recruit": "Стати рекрутом",
        "btn_steam": "Прив’язати Steam ID",

        # Ігрові ролі
        "game_roles_title": "Вибір ігрових ролей",
        "game_roles_body": "Натискайте на кнопки, щоб отримати або зняти роль.",
        "game_role_added": "Роль **{role}** видано.",
        "game_role_removed": "Роль **{role}** знято.",
        "no_game_roles": "Ігрові ролі ще не налаштовані.",

        "game_roles_panel_title": "Ігрові ролі",
        "game_roles_panel_body": (
            "Натисни кнопку нижче, щоб відкрити меню ігрових ролей.\n"
            "У ньому можна вмикати й вимикати ролі по кнопках."
        ),

        # Помилки
        "guild_not_found": "Сервер не знайдено. Звернися до адміністрації.",
        "not_in_guild": "Я не можу знайти тебе на сервері. Перезайди або напиши модераторам.",

        "role_panel_title": "Панель ролей",
        "role_panel_body": (
            "Тут можна обрати ігрові ролі, спеціалізації для ARMA-операцій "
            "і запустити процес рекрутингу."
        ),
        "role_panel_games_header": "Ігрові ролі",
        "role_panel_arma_header": "Ролі для ARMA-операцій",

        "btn_games_panel": "Отримати роль гри",
        "btn_arma_panel": "Отримати роль по ARMA",

        "no_roles_configured": "У конфігурації бота не налаштовані ролі.",
        "no_arma_roles": "Ролі для ARMA-операцій не налаштовані.",

        "arma_roles_title": "Ролі для ARMA-операцій",
        "arma_roles_body": (
            "Ці ролі доступні тільки схваленим рекрутам (статус DONE).\n"
            "Використовуються для позначення бажаної ролі на операціях."
        ),
        "arma_roles_not_done": (
            "Ролі за ARMA-посадами доступні лише рекрутам зі статусом **DONE**.\n"
            "Спочатку завершіть рекрут-процес, потім поверніться до цієї панелі."
        ),
        "arma_role_not_found": "Ця роль для ARMA-операцій не налаштована або була видалена.",
        "arma_role_added": "Роль для ARMA-операцій **{role}** видано.",
        "arma_role_removed": "Роль для ARMA-операцій **{role}** знято.",
        "notify_dm_disabled": (
            "{member}, увімкніть приватні повідомлення, щоб я міг надіслати інструкції по онбордингу. "
            "Після цього надішліть команду `{command}` на сервері."
        ),
    },
}


def t(lang: str, key: str) -> str:
    """Simple translation helper."""
    data = LANGS.get(lang) or LANGS["en"]
    return data.get(key) or LANGS["en"].get(key, key)






