from models.storage_engine.connect_db import ConnectMysqlDB  # type: ignore
from models.storage_engine.db import DBStorage  # type: ignore
storage = None
if __name__ == "models.storage_engine":
    """Instantiate and initialize the DBStorage if connection was successful"""
    db_connection = ConnectMysqlDB()
    if ConnectMysqlDB.has_connected():
        storage = DBStorage()
        storage.reload()

    else:
        print("Failed to connect to the database. DBStorage not initialized.")
