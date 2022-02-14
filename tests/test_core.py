import json
import random
import pytest
from shutil import rmtree

from contacts.core import (
    find_contact,
    get_contact,
    get_next_id,
    init_db,
    get_data,
    remove_contact,
    save_data,
    add_contact,
    update_contact,
)

MOCKED_DB_PATH = ".tests"
MOCKED_DB_FILE_PATH = ".tests/test-db.json"


def empty_db():
    with open(MOCKED_DB_FILE_PATH, "w") as test_file:
        json.dump([], test_file, indent=4)


@pytest.fixture
def demo_data():
    return [
        {
            "id": 1,
            "first_name": "Sam",
            "last_name": "Anderson",
            "sex": "male",
            "address": "California, USA",
        },
        {
            "id": 2,
            "first_name": "Jane",
            "last_name": "Smith",
            "sex": "female",
            "address": "California, USA",
        },
    ]


@pytest.fixture
def db(monkeypatch):
    monkeypatch.setattr("contacts.core.DB_FILE_PATH", MOCKED_DB_FILE_PATH)
    monkeypatch.setattr("contacts.core.DB_PATH", MOCKED_DB_PATH)

    yield init_db()

    empty_db()


@pytest.mark.usefixtures("db", "demo_data")
class TestCore:
    def test_database_init(self):
        rmtree(MOCKED_DB_PATH)
        result = init_db()
        assert result == True

    def test_get_data_returns_data(self):
        db = get_data()

        assert isinstance(db, list) == True

    def test_data_is_saved_as_expected(self, db):
        data1 = [{"test": "OK"}]
        save_data(data=data1)
        data = get_data()
        print(data)

        assert data1 == data

        data2 = [{"test": "OK"}, {"anotherTest": "OK"}]
        save_data(data=data2)
        data = get_data()

        assert data2 == data

    def test_next_id_is_generated_as_expected(self):
        # generate random list of numbers
        ids = random.sample(range(1, 101), 100)
        # generate test data
        data = [{"id": id} for id in ids]

        next_id = get_next_id(data=data)

        assert next_id == 101

    def test_contact_can_be_added(self, db):
        res1 = add_contact(
            first_name="Samar",
            last_name="Shrestha",
            sex="male",
            address="Michigan, USA",
        )

        res2 = add_contact(
            first_name="Sajal",
            last_name="Shrestha",
            sex="male",
            address="Michigan, USA",
        )

        data = get_data()
        assert res1 in data
        assert res2 in data


# @patch("core.DB_FILE_PATH", MOCKED_DB_FILE_PATH)
# @patch("core.DB_PATH", MOCKED_DB_PATH)
# class ContactTestCase(TestCase):
#     def setUp(self):
#         self.demo_data = [
#             {
#                 "id": 1,
#                 "first_name": "Sam",
#                 "last_name": "Anderson",
#                 "sex": "male",
#                 "address": "California, USA",
#             },
#             {
#                 "id": 2,
#                 "first_name": "Jane",
#                 "last_name": "Smith",
#                 "sex": "female",
#                 "address": "California, USA",
#             },
#         ]
#         init_db()

#     def tearDown(self):
#         with open(MOCKED_DB_FILE_PATH, "w") as test_file:
#             json.dump([], test_file, indent=4)

#     def test_database_initialization(self):
#         rmtree(MOCKED_DB_PATH)
#         result = init_db()
#         self.assertTrue(result)

#     def test_get_data_returns_data(self):
#         db = get_data()

#         self.assertIsInstance(db, list)

#     def test_data_is_saved_as_expected(self):
#         data1 = [{"test": "OK"}]
#         save_data(data=data1)
#         data = get_data()

#         self.assertEqual(data1, data)

#         data2 = [{"test": "OK"}, {"anotherTest": "OK"}]
#         save_data(data=data2)
#         data = get_data()

#         self.assertEqual(data2, data)

#     def test_next_id_is_generated_as_expected(self):
#         # generate random list of numbers
#         ids = random.sample(range(1, 101), 100)
#         # generate test data
#         data = [{"id": id} for id in ids]

#         next_id = get_next_id(db=data)

#         self.assertEqual(next_id, 101)

#     def test_contact_can_be_added(self):
#         res1 = add_contact(
#             first_name="Samar",
#             last_name="Shrestha",
#             sex="male",
#             address="Michigan, USA",
#         )

#         res2 = add_contact(
#             first_name="Sajal",
#             last_name="Shrestha",
#             sex="male",
#             address="Michigan, USA",
#         )

#         data = get_data()

#         self.assertIn(res1, data)
#         self.assertIn(res2, data)

#     def test_contact_can_be_retrieved_by_id(self):
#         save_data(data=self.demo_data)

#         res = get_contact(id=1)

#         self.assertEqual(res, self.demo_data[0])

#     def test_contact_can_be_updated(self):
#         save_data(data=self.demo_data)
#         res = update_contact(id=1, first_name="Sami")
#         self.assertEqual(res["first_name"], "Sami")

#     def test_contact_can_be_deleted(self):
#         save_data(data=self.demo_data)

#         res = remove_contact(1)

#         self.assertEqual(res, self.demo_data[0])
#         self.assertFalse(get_contact(1))

#     def test_contact_can_be_searched(self):
#         save_data(data=self.demo_data)

#         res = find_contact(keyword="Anderson")
#         self.assertEqual(res, self.demo_data[0])
