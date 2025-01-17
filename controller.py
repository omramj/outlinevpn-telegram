from settings import (
        BOT_API_TOKEN,
        DEFAULT_SERVER_ID,
        )
import telegram.monitoring as monitoring
import outline.api as outline
import amnezia.controller as amnezia
from settings import BOT_API_TOKEN, DEFAULT_SERVER_ID, BLACKLISTED_CHAT_IDS, ADMIN_CHAT_ID
from helpers.exceptions import (
        KeyCreationError,
        KeyRenamingError,
        InvalidServerIdError,
        InvalidGenaProfileLink
        )
import telegram.message_formatter as f
from helpers.aliases import ServerId


assert BOT_API_TOKEN is not None
    

def create_new_key(message, server_id: ServerId = DEFAULT_SERVER_ID,
                   key_name: str | None = None, type: str = "outline"):

    try:
        if key_name is None:
            key_name = form_key_name(message)

        if type == "outline":
            key = outline.get_new_key(key_name, server_id)

        elif type == "amnezia-warp":
            key = amnezia.generate_amnezia_key(type=type);
        else:
            #TODO
            print("Key type is unknown.")
            raise Exception

        return key


    except KeyCreationError:
        error_message = "API error: cannot create the key"
        send_monitoring_error_message(message, error_message)
        print(error_message)
        raise KeyCreationError

    except KeyRenamingError:
        error_message = "API error: cannot rename the key"
        send_monitoring_error_message(message, error_message)
        print(error_message)
        raise KeyRenamingError
    
    except InvalidGenaProfileLink:
        error_message = "Не удалось прочитать ссылку. Убедитесь, что:" + \
        "\n- Это ссылка на профиль в гене вида 'https://portal.itgen.io/profile/pXJnTMuEDANov9sMY'." + \
        "\n- Ссылка начинается с 'https://'."
        send_monitoring_error_message(message, error_message)
        print(error_message)
        raise InvalidGenaProfileLink

    except InvalidServerIdError:
        error_message = "The server id does not exist."
        send_monitoring_error_message(message, error_message)
        print(error_message)
        raise InvalidServerIdError
        

def form_key_name(message) -> str:
    if message.text.startswith("https://portal.itgen.io/"):
        key_name = _get_gena_user_id_from_link(message.text)
    else:
        key_name = message.from_user.username

    return key_name


def report_blacklist_attempt(username: str, chat_id: str) -> None:
    monitoring.report_blacklist_attempt(username, chat_id)


def report_not_in_whitelist(username: str, chat_id: str) -> None:
    monitoring.report_not_in_whitelist(username, chat_id)


def send_api_status():
    monitoring.send_api_status()


def send_monitoring_start_message():
    monitoring.send_start_message()


def send_monitoring_error_message(message, error_message):
    monitoring.send_error(error_message=error_message,
                          username=message.from_user.username,
                          firstname=message.from_user.first_name,
                          lastname=message.from_user.last_name)


def send_monitoring_new_key_created(key, message):
    monitoring.new_key_created(
            key_id=key.kid,
            key_name=key.name,
            chat_id=message.chat.id,
            username=message.from_user.username,
            server_id=key.server_id)


def _get_gena_user_id_from_link(link: str) -> str:
    if not link.startswith("https://portal.itgen.io/profile/"):
        raise InvalidGenaProfileLink

    gena_profile_id = link.split('/')[-1]

    # in case we have something like '?tab=home' at the end
    return gena_profile_id.split("?")[0]
