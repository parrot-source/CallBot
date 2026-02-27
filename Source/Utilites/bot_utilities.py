from dataclasses import dataclass
from dotenv import load_dotenv
from telebot import TeleBot
from pathlib import Path
from os import getenv
import socket
import sys


@dataclass
class EnvData:
    BOT_TOKEN: str
    OWNER_ID: int


def get_env(path: str) -> EnvData:
    try:
        if Path(path).exists():
            load_dotenv(path)
            bot_token = getenv("BOT_TOKEN")
            owner_id = getenv("OWNER_ID")
            return EnvData(
                BOT_TOKEN=bot_token,
                OWNER_ID=owner_id,
            )
        else:
            with open(path, 'w') as file:
                file.write("BOT_TOKEN=\nOWNER_ID=")
            print(f"[ Information ] -> Created File '{path}' -> Put (Bot Token) And (Owner ID) Into '{path}'")
            sys.exit(1)
    except Exception as e:
        print(f"[ Error ] -> {e}")


def check_network_connection(timeout:int=10) -> bool:
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).connect(("9.9.9.9", 53))
        return True
    except Exception as e:
        print(f"[ ERROR ] -> {e}")
        return False


bot_data = get_env(path='.env')
bot = TeleBot(bot_data.BOT_TOKEN)
