from pathlib import Path
import json


def get_members(path: str, chat_id:int) -> list:
    try:
        if Path(path).exists():
            with open(path, 'r') as file:
                chats = json.load(file)
            members_data = chats.get(chat_id, [])
        else:
            print("[ Error (Get Members) ] -> File Not Found!")
            return
    except Exception as e:
        print(f"[ Error (Get Members) ] -> {e}!")
        return


def save_member_data(path:str, chat_id:int, member_id:int, bot_id:int) -> bool:
    try:
        if Path(path).exists():
            with open(path, 'r') as file:
                data = json.load(file)
            chat_data = data.get(str(chat_id), False)
            if chat_data or chat_data == []:
                if member_id in data[str(chat_id)]:
                    return False
                chat_data.append(member_id)
                data[str(chat_id)] = chat_data
                with open(path, 'w') as file:
                    json.dump(data, file, indent=4)
                return True
            else:
                data[str(chat_id)] = [member_id]
                with open(path, 'w') as file:
                    json.dump(data, file, indent=4)
                return True
        else:
            Path.mkdir("Source/BotData")
            with open(path, 'w') as file:
                json.dump({str(chat_id): [member_id]}, file, indent=4)
            print("[ Error (Save Member Data) ] -> File Was Created!")
            return False
    except Exception as e:
        print(f"[ Error (Save Member Data) ] -> {e}")
        return False


def delete_member_data(path:str, chat_id:int, member_id:int) -> bool:
    try:
        if Path(path).exists():
            with open(path, 'r') as file:
                data = json.load(file)
            chat_data = data.get(str(chat_id), [])
            if not member_id in data[str(chat_id)]:
                return False
            chat_data.remove(member_id)
            data[str(chat_id)] = chat_data
            if not chat_data:
                del data[str(chat_id)]
            with open(path, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        else:
            print("[ Error (Delete Member Data) ] -> File Not Found!")
            return False
    except Exception as e:
        print(f"[ Error (Delete Member Data) ] -> {e}")
        return False
