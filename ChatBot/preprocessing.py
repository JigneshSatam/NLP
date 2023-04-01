import json
import pickle
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def store_ingredients():
  print(f"{' Prepopulating Ingredient Data ':=^50}")

  with open("data/ingredients.json") as json_file:
    result = []
    data = json.load(json_file)
    for elem in data:
      for i in elem["ingredients"]:
        result.append(lemmatize(i))
      # result.extend(elem["ingredients"])
    pickle.dump(result, open("data/ingredients.pkl", "wb"))

    # with open("populated_ingredients.txt", "w") as f:
    # print(elem["ingredients"])
    # print("Type:", type(elem["ingredients"]))
    # for ing in elem["ingredients"]:
    #     result.append(f"{ing}")
    #     f.write(f"{ing}")
    # print(result)


def store_cuisine():
  print(f"{' Prepopulating Cuisine Data ':=^50}")
  cuisine = [
      "greek",
      "southern us",
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
      "cajun creole",
      "brazilian",
      "french",
      "japanese",
      "irish",
      "korean",
      "spanish",
      "moroccan",
  ]
  result = []
  for c in cuisine:
    result.append(lemmatize(c))
  pickle.dump(result, open("data/cuisines.pkl", "wb"))


def lemmatize(text: str):
  return lemmatizer.lemmatize(text)


if __name__ == "__main__":
  store_ingredients()
  store_cuisine()
