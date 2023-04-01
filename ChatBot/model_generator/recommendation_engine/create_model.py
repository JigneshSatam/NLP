import os
import pickle
import pandas as pd
import sqlite3 as sq
from sklearn import feature_extraction, model_selection, pipeline
from sklearn.linear_model import LogisticRegressionCV
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from model_generator.recommendation_engine.feature_engineering import process_data

CUISINE_GROUPS = [
    "brazilian",
    "british",
    "cajun_creole",
    "chinese",
    "filipino",
    "french",
    "greek",
    "indian",
    "irish",
    "italian",
    "jamaican",
    "japanese",
    "korean",
    "mexican",
    "moroccan",
    "russian",
    "southern_us",
    "spanish",
    "thai",
    "vietnamese",
]
MODEL_BASE_PATH = "models/nlp"
EMBEDDING_BASE_PATH = os.path.join(MODEL_BASE_PATH, "similarity_embeddings")
os.makedirs(MODEL_BASE_PATH, exist_ok=True)
os.makedirs(EMBEDDING_BASE_PATH, exist_ok=True)


def save_pickle_file(datafile, filename):
  with open(filename, "wb") as f:
    pickle.dump(datafile, f)


def create_model_cuisine_predictions():
  data = process_data()

  model = pipeline.Pipeline(
      [
          ("vectorizer", feature_extraction.text.TfidfVectorizer()),
          ("classifier", LogisticRegressionCV(
              cv=3, random_state=42, max_iter=300, n_jobs=-1, verbose=1
          ))
      ])

  data_train, data_test = model_selection.train_test_split(
      data, test_size=0.3, random_state=42
  )

  X_train = data_train["ingredients_query"]
  y_train = data_train["cuisine"]

  model.fit(X_train, y_train)
  save_pickle_file(model, os.path.join(MODEL_BASE_PATH, "pickle_model.pkl"))


def embedding_creation(data):
  data = data["ingredients_query"].tolist()
  tagged_data = [
      TaggedDocument(words=row.split(), tags=[str(index)])
      for index, row in enumerate(data)
  ]

  max_epochs = 20
  vec_size = 50
  alpha = 0.025

  model_embedding = Doc2Vec(
      size=vec_size, alpha=alpha, min_alpha=0.00025, min_count=1, dm=1
  )

  model_embedding.build_vocab(tagged_data)

  for epoch in range(max_epochs):
    print("iteration {0}".format(epoch))
    model_embedding.train(
        tagged_data,
        total_examples=model_embedding.corpus_count,
        epochs=model_embedding.iter,
    )
    model_embedding.alpha -= 0.0002
    model_embedding.min_alpha = model_embedding.alpha

  return model_embedding


def train_embeddings():
  db = sq.connect("recipes.db")
  cursor = db.cursor()

  for c in CUISINE_GROUPS:
    cuisine_data = pd.read_sql(get_cuisine_query(), db, params=(c,))

    mdl_embedn = embedding_creation(cuisine_data)
    save_pickle_file(mdl_embedn, os.path.join(
        EMBEDDING_BASE_PATH, f"d2v_{c}.pkl"))


def get_cuisine_query():
  return "SELECT title, instructions, ingredients, ingredients_query FROM main_recipes WHERE cuisine = ?"
