import json
from pathlib import Path
from os import path
from shutil import rmtree


class Config:
    pass


class JsonDB:
    HOME_DIR = str(Path.home())
    DB_PATH = f"{HOME_DIR}/.contacts"
    DB_FILENAME = "db.json"
    DB_FILE_PATH = f"{DB_PATH}/{DB_FILENAME}"

    def __init__(self):
        self._data = []

    def init(self):
        if path.exists(self.DB_FILE_PATH):
            # db file already exists
            return

        # create directory
        Path(self.DB_PATH).mkdir(parents=True, exist_ok=True)

        # initialize empty db file
        with open(self.DB_FILE_PATH, "w") as db_file:
            json.dump([], db_file, indent=4)

        return True

    def reset(self):
        with open(self.DB_FILE_PATH, "w") as test_file:
            json.dump([], test_file, indent=4)

    def drop(self):
        rmtree(self.DB_PATH)

    def save(self):
        with open(self.DB_FILE_PATH, "w") as db_file:
            json.dump(self.data, db_file, indent=4)

    @property
    def data(self):
        if not self._data:
            with open(self.DB_FILE_PATH) as db_file:
                self._data = json.load(db_file)

        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data
        self.save()

    def _next_id(self):

        if not len(self.data):
            return 1

        ids = [item["id"] for item in self.data]
        ids.sort()

        return ids[-1] + 1

    def get(self, id=None):
        if id is None:
            return self.data

        for contact in self.data:
            if contact["id"] == id:
                return contact
        else:
            return False

    def add(self, first_name, last_name, sex, address):
        item = {
            "id": self._next_id(),
            "first_name": first_name.capitalize(),
            "last_name": last_name.capitalize(),
            "sex": sex.capitalize(),
            "address": address.upper(),
        }

        self.data.append(item)
        self.save()

        return item

    def update(self, id, **kwargs):
        for contact in self.data:
            if contact["id"] == id:
                item = {
                    "first_name": kwargs.get(
                        "first_name", contact["first_name"]
                    ).capitalize(),
                    "last_name": kwargs.get(
                        "last_name", contact["last_name"]
                    ).capitalize(),
                    "sex": kwargs.get("sex", contact["sex"]).capitalize(),
                    "address": kwargs.get("address", contact["address"]).upper(),
                }
                contact.update(item)
                self.save()
                return contact
        else:
            return False

    def remove(self, id):
        contact = self.get(id)

        if not contact:
            return False

        index = self.data.index(contact)
        del self.data[index]

        self.save()

        return contact

    def find(self, keyword):
        for contact in self.data:
            if keyword in contact.values():
                return contact
            else:
                return False


class SqliteDB:
    pass
