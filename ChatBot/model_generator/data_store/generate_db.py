import os
import sqlite3 as sq
# import pandas as pd

from model_generator.recommendation_engine.dataset import recipes_data_import
from model_generator.recommendation_engine.feature_engineering import process_recipes
from model_generator.recommendation_engine.prediction_engine import load_pickle_data

MODEL_BASE_PATH = "models/nlp"


def create_and_populate_db():
  recipes_data = recipes_data_import()

  recipes_data = process_recipes(recipes_data)

  mdl = load_pickle_data(os.path.join(MODEL_BASE_PATH, "pickle_model.pkl"))

  recipes_data["cuisine"] = mdl.predict(
      recipes_data["ingredients_query"].tolist())

  db = sq.connect("recipes.db")

  for col in recipes_data.columns:
    recipes_data[col] = recipes_data[col].astype("str")

  recipes_data.to_sql("main_recipes", db, if_exists="replace")
