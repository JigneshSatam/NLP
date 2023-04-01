import pandas as pd
import sqlite3 as sq


def get_df_from_db(cuisine):
  db = sq.connect("recipes.db")
  sql_query = get_guery()
  return pd.read_sql(sql_query, db, params=(cuisine,))


def get_guery():
  return "SELECT title, instructions, ingredients, ingredients_query FROM main_recipes WHERE cuisine = ?"
