import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from settings import (
        BOT_API_TOKEN,
        DEFAULT_SERVER_ID,
        BLACKLISTED_CHAT_IDS,
        WHITELISTED_CHAT_IDS,
        ENABLE_BLACKLIST,
        ENABLE_WHITELIST
        )
from helpers.exceptions import (
        KeyCreationError,
        KeyRenamingError,
        InvalidServerIdError
        )
import controller as ctl
from settings import BOT_API_TOKEN, DEFAULT_SERVER_ID, BLACKLISTED_CHAT_IDS, ADMIN_CHAT_ID
import telegram.message_formatter as f


assert BOT_API_TOKEN is not None
bot = AsyncTeleBot(BOT_API_TOKEN, parse_mode='HTML')


def authorize(func):
    def wrapper(message):

        chat_id_to_check = message.chat.id

        if ENABLE_BLACKLIST and str(chat_id_to_check) in BLACKLISTED_CHAT_IDS:
            ctl.report_blacklist_attempt(message.from_user.username,
                                                chat_id_to_check)
            return

        if ENABLE_WHITELIST and str(chat_id_to_check) not in WHITELISTED_CHAT_IDS:
            ctl.report_not_in_whitelist(message.from_user.username,
                                                chat_id_to_check)
            return

        return func(message)
    return wrapper


@bot.message_handler(commands = ['status'])
@authorize
def send_status(message):
    ctl.send_api_status()


@bot.message_handler(commands = ['start'])
@authorize
async def send_welcome(message):
    await bot.send_message(message.chat.id,
    "Hey! This bot is used for creating Outline keys.",
    reply_markup = _make_main_menu_markup())

    
@bot.message_handler(commands = ['help'])
@authorize
async def send_help(message):
    await bot.send_message(message.chat.id, f.make_help_message())


@bot.message_handler(commands = ['servers'])
@authorize
async def send_servers_list(message):
    await bot.send_message(message.chat.id, f.make_servers_list())


@bot.message_handler(content_types = ['text'])
@authorize
async def anwser(message):

    try:
        if message.text == "New Outline Key":
            key = ctl.create_new_key(message)
            await _send_key(message, key)
            
        elif message.text == "WARP for AmneziaVPN":
            if _user_is_admin(message):
                key = ctl.create_new_key(message, type="amnezia-warp")
                await _send_key(message, key)

        elif message.text.startswith("https://portal.itgen.io/"):
            key = ctl.create_new_key(message)
            await _send_key(message, key)

        elif message.text == "Downloads":
            await bot.send_message(message.chat.id,
                             f.make_download_message(),
                             disable_web_page_preview=True
                             )

        elif message.text == "Help":
            await bot.send_message(message.chat.id, f.make_help_message())

        elif message.text[:7] == "/newkey":
            server_id, key_name = _parse_newkey_command(message)
            key = ctl.create_new_key(message, server_id, key_name)
            await _send_key(message, key)

        else:
            await bot.send_message(message.chat.id,
                    "Unknown command.",
                    reply_markup = _make_main_menu_markup())

    # TODO: logging
    except KeyCreationError or KeyRenamingError:
        error_message = "Sorry, there is an error on our side. Could not create a key for you"
        print(error_message)
        await _send_error(message, error_message)

    except InvalidServerIdError:
        error_message = "The server id does not exist."
        print(error_message)
        await _send_error(message, error_message)
        raise InvalidServerIdError
                

async def _send_key(message, key):

    text = f.make_message_for_new_key(key)

    await bot.send_message(
            message.chat.id,
            text
            )
    ctl.send_monitoring_new_key_created(key, message)


async def _send_error(message, error_text):

    await bot.send_message(
            message.chat.id,
            error_text
            )


def _make_main_menu_markup() -> types.ReplyKeyboardMarkup:
    menu_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    
    keygen_server1_button = types.KeyboardButton("New Outline Key")
    keygen_awg_warp_button = types.KeyboardButton("WARP for AmneziaVPN")
    download_button = types.KeyboardButton("Downloads")
    help_button = types.KeyboardButton("Help")

    menu_markup.add(
            keygen_server1_button,
            keygen_awg_warp_button,
            download_button,
            help_button
            )
    return menu_markup


def _parse_newkey_command(message) -> list:
    arguments = message.text[8:].split()

    if arguments != []:
        server_id = arguments[0]
    else:
        server_id = DEFAULT_SERVER_ID

    key_name = ''.join(arguments[1:])

    if key_name == '': 
        key_name = ctl.form_key_name(message)
    
    return [server_id, key_name]


def _user_is_admin(message) -> bool:

    if str(message.chat.id) == str(ADMIN_CHAT_ID):
        return True

    return False


def start_telegram_server():
    ctl.send_monitoring_start_message()
    asyncio.run(bot.infinity_polling())
