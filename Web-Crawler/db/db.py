import sqlite3
from sqlite3 import Connection, Error


class Database:
  db_file: str = "data.sqlite"

  @staticmethod
  def create_connection() -> Connection:
    """ create a database connection to the SQLite database

    :return: Connection object or None
    """
    conn = None
    try:
      conn = sqlite3.connect(Database.db_file)
    except Error as e:
      print("Error in connection.")
      print(e)

    return conn

  @staticmethod
  def create_table(create_table_statement) -> None:
    """ create a table from the create_table_statement

    :param create_table_statement: a CREATE TABLE statement
    :return:
    """
    try:
      conn = Database.create_connection()
      c = conn.cursor()
      c.execute(create_table_statement)
    except Error as e:
      print("Error in table creation.")
      print(e)

    conn.close()
