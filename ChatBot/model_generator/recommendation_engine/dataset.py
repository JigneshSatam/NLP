import os
import pandas as pd

CUISINE_PATH = "data/cuisine_data/"
RECIPES_PATH = "data/recipes_data/"
recipes_ar_file = "recipes_raw_nosource_ar.json"
recipes_epi_file = "recipes_raw_nosource_epi.json"
recipes_fn_file = "recipes_raw_nosource_fn.json"


def recipes_data_import():
  ar = os.path.join(RECIPES_PATH, recipes_ar_file)
  epi = os.path.join(RECIPES_PATH, recipes_epi_file)
  fn = os.path.join(RECIPES_PATH, recipes_fn_file)

  recipes = pd.concat(
      [
          pd.read_json(ar, orient="index"),
          pd.read_json(epi, orient="index"),
          pd.read_json(fn, orient="index"),
      ]
  )

  recipes = recipes.reset_index()
  recipes = recipes.drop(columns=["picture_link", "index"])
  return recipes


cuisine_train_file = "train.json"
cuisine_test_file = "test.json"


def cuisine_data_import():
  cuisine_train = pd.read_json(os.path.join(CUISINE_PATH, cuisine_train_file))
  cuisine_test = pd.read_json(os.path.join(CUISINE_PATH, cuisine_test_file))
  return pd.concat([cuisine_train, cuisine_test], axis=0)
