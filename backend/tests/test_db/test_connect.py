# """Module for testing creating database and inserting table in it"""

import unittest
from unittest.mock import patch

from app.models.storage_engine import DBStorage, storage  # type ignore
from app.models.storage_engine.connect_db import ConnectMysqlDB


class TestCreateDB(unittest.TestCase):
    """Test creation of Database"""

    @patch.dict(
        "os.environ",
        {
            "MYSQL_USER": "root",
            "MYSQL_PWD": "root",
            "MYSQL_HOST": "localhost",
            "MYSQL_DB": "test_db0001",
        },
    )
    def test_CreateDB(self):
        """Test if the instance of the database has been established"""
        ConnectMysqlDB.create_database_if_not_exists()
        self.assertTrue(ConnectMysqlDB.has_connected())


class TestDb(unittest.TestCase):
    """Class for inserting the table into the databases"""

    @patch.dict(
        "os.environ",
        {
            "MYSQL_USER": "root",
            "MYSQL_PWD": "root",
            "MYSQL_HOST": "localhost",
            "MYSQL_DB": "test_db0001",
        },
    )
    def test_db_doc_string(self):
        """Test if  method and some doc string exist"""
        doc = storage
        self.assertIsNotNone(doc.__doc__)
        self.assertIsNotNone(doc.get_engine.__doc__)
        self.assertIsNotNone(doc.reload.__doc__)
        self.assertIsNotNone(doc.save.__doc__)

    def test_method(self):
        """Test if the following methog exist"""
        self.assertTrue(hasattr(storage, "reload"))
        self.assertTrue(hasattr(storage, "save"))
        self.assertTrue(hasattr(storage, "get_instance"))

    def test_reload(self):
        """Test reload method. if session of db has started"""
        self.assertIsInstance(storage, DBStorage)


if __name__ == "__main__":
    import sys
    print(sys.path, "WHER")

    unittest.main()
