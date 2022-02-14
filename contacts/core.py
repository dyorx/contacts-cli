import json
from pathlib import Path
from os import path
from shutil import rmtree

HOME_DIR = str(Path.home())
DB_PATH = f"{HOME_DIR}/.contacts"
DB_FILENAME = "db.json"
DB_FILE_PATH = f"{DB_PATH}/{DB_FILENAME}"


def init_db():
    if path.exists(DB_FILE_PATH):
        # db file already exists
        return

    # create directory
    Path(DB_PATH).mkdir(parents=True, exist_ok=True)

    # initialize empty db file
    with open(DB_FILE_PATH, "w") as db_file:
        json.dump([], db_file, indent=4)

    return True


def reset_db():
    with open(DB_FILE_PATH, "w") as test_file:
        json.dump([], test_file, indent=4)


def drop_db():
    rmtree(DB_FILE_PATH)


def get_data():
    with open(DB_FILE_PATH) as db_file:
        db = json.load(db_file)
        return db


def save_data(data):
    with open(DB_FILE_PATH, "w") as db_file:
        json.dump(data, db_file, indent=4)


def get_next_id(data):
    if not len(data):
        return 1

    ids = [item["id"] for item in data]
    ids.sort()
    return ids[-1] + 1


def add_contact(first_name, last_name, sex, address):
    data = get_data()

    item = {
        "id": get_next_id(data),
        "first_name": first_name.capitalize(),
        "last_name": last_name.capitalize(),
        "sex": sex.capitalize(),
        "address": address.upper(),
    }

    data.append(item)
    save_data(data)

    return item


def get_contact(id=None):
    data = get_data()
    if id is None:
        return data

    for contact in get_data():
        if contact["id"] == id:
            return contact
    else:
        return False


def update_contact(id, **kwargs):
    data = get_data()

    for contact in data:
        if contact["id"] == id:
            item = {
                "first_name": kwargs.get(
                    "first_name", contact["first_name"]
                ).capitalize(),
                "last_name": kwargs.get("last_name", contact["last_name"]).capitalize(),
                "sex": kwargs.get("sex", contact["sex"]).capitalize(),
                "address": kwargs.get("address", contact["address"]).upper(),
            }
            contact.update(item)
            save_data(data)
            return contact
    else:
        return False


def remove_contact(id):
    contact = get_contact(id)

    if not contact:
        return False

    data = get_data()
    index = data.index(contact)
    del data[index]

    save_data(data=data)

    return contact


def find_contact(keyword):
    for contact in get_data():
        if keyword in contact.values():
            return contact
    else:
        return False
