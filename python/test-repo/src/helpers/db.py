from typing import Any, Generator

import psycopg2  # type: ignore
from psycopg2.extensions import connection, cursor  # type: ignore

from src.core.exceptions import ThirdPartyError


class Postgre:
    def __init__(
        self, *, user: str, password: str, host: str, port: str, db_name: str
    ) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name

    def get_db(self) -> Generator[cursor, Any, Any]:
        """
        Create a database connection of our choosing.

        Raises:
            ThirdPartyError: will be raised if the application fail to
                connect to postgresql.

        Yields:
            Generator: database cursor to interact with the database
        """
        cursor, db = None, None
        try:
            db = self.create_connection()
            cursor = db.cursor()
            yield cursor
        except psycopg2.Error as exc:
            raise ThirdPartyError(f"Fail to create connection to database: {exc}")
        finally:
            if db and cursor:
                cursor.close()
                db.close()

    def create_connection(self) -> connection:
        """
        Establishes a connection to a PostgreSQL database using Psycopg2.

        This function uses predefined variables for the host, username,
        password, and database name.
        It sets the character set to 'utf8mb4' to support a wide range of
        characters, and uses a dictionary cursor, which allows access to
        rows as Python dictionaries.

        Returns:
            connection: A Psycopg2 connection object that can be used to
            interact with the database.
        """
        return psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            dbname=self.db_name,
        )
