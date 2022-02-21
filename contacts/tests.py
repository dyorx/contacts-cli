from unittest import TestCase, main
from unittest.mock import patch
from contacts import JsonDB
from shutil import rmtree
from os import remove

MOCK_DB_PATH = ".tests"
MOCK_DB_FILE_PATH = f"{MOCK_DB_PATH}/db.json"


@patch("contacts.core.JsonDB.DB_PATH", MOCK_DB_PATH)
@patch("contacts.core.JsonDB.DB_FILE_PATH", MOCK_DB_FILE_PATH)
class JsonDBTestCase(TestCase):
    def setUp(self):
        self.db = JsonDB()
        self.db.init()

    def tearDown(self):
        self.db.reset()

    def test_database_can_be_initialized(self):
        rmtree(MOCK_DB_PATH)
        result = self.db.init()

        self.assertTrue(result)

    def test_contact_can_be_added(self):
        test_data = {
            "first_name": "Sam",
            "last_name": "Shr",
            "sex": "Male",
            "address": "USA",
        }
        res = self.db.add(**test_data)

        self.assertIn(res, self.db.data)


class SqliteDBTestCase(TestCase):
    def test_database_is_instantiated_properly(self):
        self.assertTrue(False)

    def test_contact_can_be_added(self):
        self.assertTrue(False)


if __name__ == "__main__":
    main()
