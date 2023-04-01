import re
import nltk
from nltk.corpus import stopwords

from model_generator.recommendation_engine.dataset import cuisine_data_import

import ssl
try:
  _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
  pass
else:
  ssl._create_default_https_context = _create_unverified_https_context

nltk.download("wordnet")
nltk.download("stopwords")


additional_stop_words = [
    "advertisement",
    "advertisements",
    "cup",
    "cups",
    "tablespoon",
    "tablespoons",
    "teaspoon",
    "teaspoons",
    "ounce",
    "ounces",
    "salt",
    "pepper",
    "pound",
    "pounds",
]


def text_preprocessing_utility(text, stemming_flag=False, lemmatizing_flag=True, stopwords_list=None):
  text = re.sub(r"[^\w\s]", "", str(text).lower().strip())

  text_tokens = text.split()

  if stopwords_list is not None:
    text_tokens = [word for word in text_tokens if word not in stopwords_list]

  if stemming_flag == True:
    porter_stemmer = nltk.stem.porter.PorterStemmer()
    text_tokens = [porter_stemmer.stem(word) for word in text_tokens]

  if lemmatizing_flag == True:
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    text_tokens = [lemmatizer.lemmatize(word) for word in text_tokens]

  text = " ".join(text_tokens)
  text = "".join([i for i in text if not i.isdigit()])
  text = re.sub(" +", " ", text)
  return text


def process_data():
  dataset = cuisine_data_import()

  def internal_processing(row):
    return " ".join(row["ingredients"])

  dataset["ingredients"] = dataset.apply(
      lambda x: internal_processing(x), axis=1)
  dataset.dropna(inplace=True)
  dataset = dataset.drop(columns=["id"]).reset_index(drop=True)

  stop_word_list = stopwords.words("english")
  stop_word_list.extend(additional_stop_words)

  dataset["ingredients_query"] = dataset["ingredients"].apply(
      lambda x: text_preprocessing_utility(
          x, stemming_flag=False, lemmatizing_flag=True, stopwords_list=stop_word_list
      )
  )
  return dataset


def process_recipes(data):
  stop_word_list = stopwords.words("english")
  stop_word_list.extend(additional_stop_words)

  data["ingredients_query"] = data["ingredients"].apply(
      lambda x: text_preprocessing_utility(
          x, stemming_flag=False, lemmatizing_flag=True, stopwords_list=stop_word_list
      )
  )
  return data


def get_tokenize_text(input_text):
  stop_word_list = stopwords.words("english")
  stop_word_list.extend(additional_stop_words)

  return text_preprocessing_utility(
      input_text, stemming_flag=False, lemmatizing_flag=True, stopwords_list=stop_word_list
  )
