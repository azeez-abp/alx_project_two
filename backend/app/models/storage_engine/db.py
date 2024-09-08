#!/usr/bin/python3
"""
Enterprise-level implementation of DBStorage class to interact with a MySQL database.
"""

import logging
from os import getenv
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from contextlib import contextmanager

# Initialize Base for model declarations
Base = declarative_base()

# Load environment variables securely
MYSQL_USER = getenv("MYSQL_USER")
MYSQL_PWD = getenv("MYSQL_PWD")
MYSQL_HOST = getenv("MYSQL_HOST")
MYSQL_DB = getenv("MYSQL_DB")
APP_ENV = getenv("APP_ENV", "development")

# Configure logging for enterprise-level code
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DBStorage:
    """Manages MySQL database operations for the application"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage object and
        configure the database engine.
        """
        try:
            logger.info("Initializing DBStorage...")
            self.__engine = create_engine(
                f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}/{MYSQL_DB}",
                pool_pre_ping=True,
                echo=False  # Disable SQL echo in production for performance and security
            )
            
            if APP_ENV == "test":
                # Drop all tables in test environment for fresh testing
                Base.metadata.drop_all(self.__engine)
                logger.info("Dropped all tables in test environment.")

        except exc.SQLAlchemyError as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise

    def reload(self):
        """Load all database tables and create a new session."""
        try:
            logger.info("Reloading database schema and initializing session...")
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
            self.__session = scoped_session(session_factory)
        except exc.SQLAlchemyError as e:
            logger.error(f"Error reloading the database: {str(e)}")
            raise

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.__session()
        try:
            yield session
            session.commit()
        except Exception as e:
            logger.error(f"Session rollback due to: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()

    def save(self, obj=None):
        """Commit changes for the current session. If object is passed, add it to the session."""
        try:
            with self.session_scope() as session:
                if obj:
                    session.add(obj)
                logger.info("Changes committed successfully.")
        except exc.SQLAlchemyError as e:
            logger.error(f"Error committing changes: {str(e)}")
            raise

    def get(self, model, id):
        """Retrieve one object by its primary key (id)."""
        try:
            with self.session_scope() as session:
                obj = session.query(model).get(id)
                if obj:
                    logger.info(f"Retrieved object {obj} with ID {id}.")
                else:
                    logger.warning(f"No object found with ID {id}.")
                return obj
        except exc.SQLAlchemyError as e:
            logger.error(f"Error retrieving object: {str(e)}")
            raise

    def get_all(self, model):
        """Retrieve all objects of a certain type (model)."""
        try:
            with self.session_scope() as session:
                objects = session.query(model).all()
                logger.info(f"Retrieved {len(objects)} objects.")
                return objects
        except exc.SQLAlchemyError as e:
            logger.error(f"Error retrieving objects: {str(e)}")
            raise

    def delete(self, obj=None):
        """Delete an object from the current session."""
        try:
            with self.session_scope() as session:
                if obj:
                    session.delete(obj)
                    logger.info(f"Deleted object {obj}.")
        except exc.SQLAlchemyError as e:
            logger.error(f"Error deleting object: {str(e)}")
            raise

    def close(self):
        """Close the current session."""
        try:
            self.__session.remove()
            logger.info("Session closed successfully.")
        except exc.SQLAlchemyError as e:
            logger.error(f"Error closing session: {str(e)}")
            raise

    def get_engine(self):
        """Return the database engine."""
        return self.__engine

    def get_instance(self):
        """
        Return the current session instance for direct execution of SQL or other
        complex operations that require access to the session.
        """
        if self.__session:
            return self.__session
        else:
            raise RuntimeError("Session is not initialized. Call reload() to initialize the session.")
