from settings import (
    OUTLINE_WINDOWS_DOWNLOAD_LINK,
    OUTLINE_MACOS_DOWNLOAD_LINK,
    OUTLINE_LINUX_DOWNLOAD_LINK,
    OUTLINE_CHOMEOS_DOWNLOAD_LINK,
    OUTLINE_IOS_DOWNLOAD_LINK,
    OUTLINE_ANDROID_DOWNLOAD_LINK,
    OUTLINE_ANDROID_APK_DOWNLOAD_LINK,
    servers
    )
from helpers.aliases import ServerId
from helpers.classes import TextKey
from textwrap import dedent


def make_message_for_new_key(key: TextKey) -> str:
   #print(f"message_formatter: type: {type}")
   if key.type == "outline":
      message_to_send = dedent(
   f"""Your key:
      \n<code>{key.access_string}</code>
      \nTap to copy.
      \nServer is located in: <b>{servers[key.server_id].location}</b>
      \nThis key should be pasted to <b>Outline Client.</b>
      """)

   elif key.type == "amnezia-warp":

      message_to_send = dedent(
   f"""Your key:
      \n<code>{key.access_string}</code>
      \nTap to copy.
      \nThis key should be pasted to <b>AmneziaVPN</b> or <b>AmneziaWG.</b>
      """)

   else:
      # TODO
      print("message_formatter: got an unknown app type.")
      raise Exception

   return message_to_send


def make_download_message() -> str:
    message_to_send = dedent(
    f"""
   <a href="https://github.com/amnezia-vpn/amnezia-client/releases">Download AmneziaVPN</a>
   <a href="{OUTLINE_WINDOWS_DOWNLOAD_LINK}">Outline for Windows</a>
   <a href="{OUTLINE_MACOS_DOWNLOAD_LINK}">Outline for MacOS</a>
   <a href="{OUTLINE_LINUX_DOWNLOAD_LINK}">Outline for Linux</a>
   <a href="{OUTLINE_CHOMEOS_DOWNLOAD_LINK}">Outline for ChromeOS</a>
   <a href="{OUTLINE_IOS_DOWNLOAD_LINK}">Outline for iOS</a>
   <a href="{OUTLINE_ANDROID_DOWNLOAD_LINK}">Outline for Android</a>
   <a href="{OUTLINE_ANDROID_APK_DOWNLOAD_LINK}">Outine for Android (APK)</a>
    """)
    return message_to_send


def make_help_message() -> str:

    message_to_send = "The help message is temporarily on vacation."


    return message_to_send


def make_servers_list() -> str:

    message_to_send = ""
    for server_id, server in servers.items():
        message_to_send += f'server_id: {server_id}, location: {server.location}\n'
    return message_to_send
