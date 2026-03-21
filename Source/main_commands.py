from Source.Utilites.bot_utilities import bot, bot_data, check_network_connection
from Source.files import save_member_data, delete_member_data, get_members
from pathlib import Path
import logging
import shutil
import json


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@bot.message_handler(commands=['help'])
def show_help(message) -> None:
    text = "HELP:\n\nHello, my name is 'CallBot'\nI can call members of a chat!\n\nYou can use commands:\n/in - (to get notifications)\n/out - (to stop get notifications)\n/system - (to check if you are in system)\n/all - (to call members)!"
    bot.reply_to(message=message, text=text, parse_mode="Markdown")


@bot.message_handler(commands=['in'])
def add_member(message) -> None:
    text = "Now you will be notified!"
    if is_group(message=message):
        if save_member_data(path="Source/BotData/chats.json", chat_id=message.chat.id, member_id=message.from_user.id, bot_id=bot.get_me().id):
            bot.reply_to(message=message, text=text, parse_mode="Markdown")


@bot.message_handler(commands=['out'])
def remove_member(message) -> None:
    text = "Now you will not be notified!"
    if is_group(message=message):
        if delete_member_data(path="Source/BotData/chats.json", chat_id=message.chat.id, member_id=message.from_user.id):
            bot.reply_to(message=message, text=text, parse_mode="Markdown")


@bot.message_handler(commands=['system'])
def check_member(message) -> None:
    if is_group(message=message):
        text = "You are not in system!"
        path = "Source/BotData/chats.json"
        chat_data = get_members(path=path, chat_id=str(message.chat.id))
        if message.from_user.id in chat_data:
            text = "You are in system!"
        bot.reply_to(message=message, text=text, parse_mode="Markdown")


@bot.message_handler(commands=['all'])
def call_all_members(message) -> None:
    if is_group(message=message):
        text = "Call Members!"
        path = "Source/BotData/chats.json"
        chat_data = get_members(path=path, chat_id=str(message.chat.id))
        for member_id in chat_data:
            text += f"<a href='tg://user?id={member_id}'>\u200B</a>"
        bot.reply_to(message=message, text=text, parse_mode="HTML")


@bot.message_handler(commands=['debug'])
def check_bot_health(message) -> None:
    if int(message.from_user.id) != int(bot_data.OWNER_ID):
        return
    path = 'Source/BotData/chats.json'
    text = "DEBUG:\n\n"
    debug_connection: bool = False
    debug_get_chat_data: bool = False
    try:
        debug_connection = check_network_connection(timeout=10)
        if Path(path).exists():
            with open(path, 'r') as file:
                data = get_members(path=path, chat_id=str(message.chat.id))
            debug_chat_data = True if data else False
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        text += f"ERROR: 'can't get data base'\n"
    except Exception as e:
        text += f"ERROR: '{e}'\n"
    text += f"Connection: {debug_connection}\nGet Chat Data: {debug_get_chat_data}"
    terminal_size = shutil.get_terminal_size().columns
    print(f"{'-'*terminal_size}\n{text}\n{'-'*terminal_size}")
    bot.reply_to(message=message, text=text, parse_mode="Markdown")


@bot.message_handler(content_types=["new_chat_members"])
def get_new_member(message) -> None:
    for member in message.new_chat_members:
        if member.is_bot:
            if member.id == bot.get_me().id:
                text = f"WARNING:\n\nYour bot was append in new group:\n\nName: {message.chat.title}\nID: {message.chat.id})\nBy: {message.from_user.id}"
                bot.send_message(chat_id=bot_data.OWNER_ID, text=text, parse_mode="Markdown")
            return
        text = f"WELCOME MESSAGE:\n\nHello, [{member.full_name}](tg://user?id={member.id})!\nCheck /help command!"
        bot.reply_to(message=message, text=text, parse_mode="Markdown")


def is_group(message:object) -> bool:
    text = "ERROR:\n\nYou are not in a group!"
    if message.chat.type in [ "group", "supergroup" ]:
        return True
    bot.reply_to(message=message, text=text, parse_mode="Markdown")
    return False
