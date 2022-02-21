import json
import random
import pytest
from shutil import rmtree
from os import path

from contacts.core import JsonDB

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
    monkeypatch.setattr("contacts.core.JsonDB.DB_FILE_PATH", MOCKED_DB_FILE_PATH)
    monkeypatch.setattr("contacts.core.JsonDB.DB_PATH", MOCKED_DB_PATH)

    db = JsonDB()
    db.init()
    yield db

    empty_db()


@pytest.mark.usefixtures("db", "demo_data")
class TestJsonDB:
    def test_database_init(self):
        rmtree(MOCKED_DB_PATH)
        db = JsonDB()
        result = db.init()
        assert result == True

    def test_database_reset(self, db):
        db.reset()

        assert len(db.data) == 0

    def test_database_can_be_dropped(self, db):
        db.drop()

        assert not path.exists(db.DB_FILE_PATH)

        db.init()

    def test_get_data_returns_data(self, db):
        data = db.data

        assert isinstance(data, list) == True

    def test_data_is_saved_as_expected(self, db):
        test_data = [{"test": "OK"}]
        db.data = test_data

        assert db.data == test_data

        test_data = [{"test": "OK"}, {"anotherTest": "OK"}]
        db.data = test_data

        assert db.data == test_data

    def test_next_id_is_generated_as_expected(self, db):
        # generate random list of numbers
        ids = random.sample(range(1, 101), 100)
        # generate test data
        db.data = [{"id": id} for id in ids]

        next_id = db._next_id()

        assert next_id == 101

    def test_contact_can_be_added(self, db):
        res1 = db.add(
            first_name="Samar",
            last_name="Shrestha",
            sex="male",
            address="Michigan, USA",
        )

        res2 = db.add(
            first_name="Sajal",
            last_name="Shrestha",
            sex="male",
            address="Michigan, USA",
        )

        assert res1 in db.data
        assert res2 in db.data

    def test_contact_can_be_updated(self, db, demo_data):
        db.data = demo_data

        db.update(1, first_name="Samar")

        assert "Samar" == db.data[0]["first_name"]

    def test_contact_can_be_removed(self, db, demo_data):
        db.data = demo_data

        db.remove(id=1)

        assert len(db.data) == 1

    def test_contact_can_be_searched(self, db, demo_data):
        db.data = demo_data

        result = db.find(keyword="Sam")

        assert result == demo_data[0]

        # must return false
        result = db.find(keyword="TestUser")

        assert result == False
