import os
import pickle

from model_generator.data_store.inference import get_df_from_db
from model_generator.recommendation_engine.feature_engineering import get_tokenize_text

MODEL_BASE_PATH = "models/nlp"
EMBEDDING_BASE_PATH = os.path.join(MODEL_BASE_PATH, "similarity_embeddings")
CUISINE_GROUPS = [
    "greek",
    "southern_us",
    "filipino",
    "indian",
    "jamaican",
    "spanish",
    "italian",
    "mexican",
    "chinese",
    "british",
    "thai",
    "vietnamese",
    "cajun_creole",
    "brazilian",
    "french",
    "japanese",
    "irish",
    "korean",
    "moroccan",
    "russian",
]


def load_pickle_data(pkl_filename):
  with open(pkl_filename, "rb") as pkl_file:
    return pickle.load(pkl_file)


def get_similar_recipes(input_text, cuisine_file, top_k=3):
  tokenize_text = get_tokenize_text(input_text).split()

  vector = load_pickle_data(os.path.join(
      EMBEDDING_BASE_PATH, f"d2v_{cuisine_file}.pkl"))

  emdbngs = vector.infer_vector(tokenize_text)
  best_match_recipes = vector.docvecs.most_similar([emdbngs])

  best_match_recipes_index = [int(output[0]) for output in best_match_recipes]

  dataframe = get_df_from_db(cuisine_file)

  return dataframe[dataframe.index.isin(best_match_recipes_index)].head(top_k)
