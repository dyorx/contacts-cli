import json
from pathlib import Path
from os import path
from shutil import rmtree


class ContactsCore:
    HOME_DIR = str(Path.home())
    DB_PATH = f"{HOME_DIR}/.contacts"
    DB_FILENAME = "db.json"
    DB_FILE_PATH = f"{DB_PATH}/{DB_FILENAME}"

    def init_db(self):
        if path.exists(self.DB_FILE_PATH):
            # db file already exists
            return

        # create directory
        Path(self.DB_PATH).mkdir(parents=True, exist_ok=True)

        # initialize empty db file
        with open(self.DB_FILE_PATH, "w") as db_file:
            json.dump([], db_file, indent=4)

        return True

    def reset_db(self):
        with open(self.DB_FILE_PATH, "w") as test_file:
            json.dump([], test_file, indent=4)

    def drop_db(self):
        rmtree(self.DB_FILE_PATH)

    def get_data(self):
        with open(self.DB_FILE_PATH) as db_file:
            db = json.load(db_file)
            return db

    def save_data(self, data):
        with open(self.DB_FILE_PATH, "w") as db_file:
            json.dump(data, db_file, indent=4)

    def get_next_id(self, data):
        if not len(data):
            return 1

        ids = [item["id"] for item in data]
        ids.sort()
        return ids[-1] + 1

    def add_contact(self, first_name, last_name, sex, address):
        data = self.get_data()

        item = {
            "id": self.get_next_id(data),
            "first_name": first_name.capitalize(),
            "last_name": last_name.capitalize(),
            "sex": sex.capitalize(),
            "address": address.upper(),
        }

        data.append(item)
        self.save_data(data)

        return item

    def get_contact(self, id=None):
        data = self.get_data()
        if id is None:
            return data

        for contact in self.get_data():
            if contact["id"] == id:
                return contact
        else:
            return False

    def update_contact(self, id, **kwargs):
        data = self.get_data()

        for contact in data:
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
                self.save_data(data)
                return contact
        else:
            return False

    def remove_contact(self, id):
        contact = self.get_contact(id)

        if not contact:
            return False

        data = self.get_data()
        index = data.index(contact)
        del data[index]

        self.save_data(data=data)

        return contact

    def find_contact(self, keyword):
        for contact in self.get_data():
            if keyword in contact.values():
                return contact
        else:
            return False
