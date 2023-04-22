import json
from sqlite3 import Error
from db.db import Database


class KnowledgeBase:

  def create_knowledge_base() -> None:

    sql_create_knowledge_base_table = """
      CREATE TABLE IF NOT EXISTS knowledge_base (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        facts text
      ); """

    try:
      # create knowledge_base table
      Database.create_table(sql_create_knowledge_base_table)
    except Error as e:
      print(e)
      print("Error! cannot create the knowledge_base table.")

  def insert(self, data: dict[list[str]]) -> None:
    """ insert all term and facts in to the knowledge_base table"""

    query = "insert into knowledge_base (name, facts) values"

    for k, v in data.items():
      query += f"('{k}', '{json.dumps(v)}'),"

    query = query.strip(",")
    query += ";"

    try:
      conn = Database.create_connection()
      conn.execute(query)
      conn.commit()
    except Error as e:
      print("Records not inserted.")
      print(e)

    conn.close()

  def find(self, term: str) -> list[str]:

    facts: list[str] = None

    query = "select facts from knowledge_base where name = '" + term + "';"
    try:
      conn = Database.create_connection()
      rows = conn.execute(query)

      for row in rows:
        facts = json.loads(row[0])
    except Error as e:
      print("Records search error.")
      print(e)

    conn.close()

    return facts

  def delete_all(self) -> None:
    query = "delete from knowledge_base;"
    try:
      conn = Database.create_connection()
      conn.execute(query)
    except Error as e:
      print("Records delete error.")
      print(e)

    conn.close()

  def select_all(self) -> None:
    query = "select facts from knowledge_base;"
    try:
      conn = Database.create_connection()
      rows = conn.execute(query)
      facts = None
      for row in rows:
        facts = json.loads(row[0])

      with open("facts.txt", "w") as f:
        for fact in facts:
          f.write(fact + " \n")
    except Error as e:
      print("Records delete error.")
      print(e)

    conn.close()


if __name__ == 'db.knowledge_base':
  KnowledgeBase.create_knowledge_base()
