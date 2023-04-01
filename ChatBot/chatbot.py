import spacy
import pickle
import random

from nltk.tokenize import word_tokenize
from preprocessing import lemmatize
from model_generator.recommendation_engine.prediction_engine import get_similar_recipes

nlp = spacy.load("en_core_web_sm")


class ChatBot:
  ingredients_dataset = set(pickle.load(open("data/ingredients.pkl", "rb")))
  cuisine_dataset = set(pickle.load(open("data/cuisines.pkl", "rb")))

  name: str = ""
  cuisineCtr: int = 0
  user: str = "User"
  ingredients = set([])
  cuisine: str = ""
  greetings = set(
      ["hi", "howdy", "hello", "nice to meet you", "hey", "what's up", "wassup"]
  )

  def __init__(self, name) -> None:
    self.name: str = name
    self.user: str = "User"

  def set_person_if_present(self, text: str) -> bool:
    entitrySet = False

    doc = nlp(text)
    for ent in doc.ents:
      if ent.label_.lower() == "person" and ent.text.lower() != self.name:
        entitrySet = True
        self.user = ent.text
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

    return entitrySet

  def get_ingredient(self, text: str):
    lemmatized_list = set([])
    for word in word_tokenize(text):
      lemmatized_list.add(lemmatize(word))
    return set([i for i in lemmatized_list if i in self.ingredients_dataset])

  def check_ingredient(self, text: str) -> bool:
    return any(self.get_ingredient(text))

  def get_cuisine(self, text: str):
    lemmatized_list = set([])
    for word in word_tokenize(text):
      lemmatized_list.add(lemmatize(word))
    return [c for c in lemmatized_list if c in self.cuisine_dataset]

  def get_random_cuisine(self):
    return random.sample(self.cuisine_dataset, 1)[0].replace(" ", "_")

  def get_random_question_for_cuisine(self):
    cuisine_questions = set(
        [
            "Are you looking for a particular cuisine?",
            "Sure! Which cuisine are you in the mood for today?",
            "What cuisine are we craving for today?",
            "Which cuisine do we feel like trying today?",
        ]
    )
    return random.sample(cuisine_questions, 1)[0]

  def get_random_question_for_cuisine_and_ingredients(self):
    cuisine_questions = set(
        [
            "Are you looking for a particular cuisine or have certain ingredients at hand?",
            "Sure! Any more details you would like to provide? Like which cuisine or certain ingredients you would like to cook with?",
            "What cuisine are we craving for today? Any ingredients that you would like to cook with?",
            "Which cuisine do we feel like trying today? Any ingredients in your pantry that you would like to use?",
        ]
    )
    return random.sample(cuisine_questions, 1)[0]

  def get_random_question_for_ingredients(self):
    cuisine_questions = set(
        [
            "Do you have certain ingredients at hand?",
            "Sure! Any more details you would like to provide? Like certain ingredients you would like to cook with?",
            "Alright! before I share some mouthwatering recipes, any ingredients that you would like to cook with?",
            "Sure, any ingredients in your pantry that you would like to use today?",
        ]
    )
    return random.sample(cuisine_questions, 1)[0]

  def check_cuisine_and_ingredients_and_return_reponse(self):
    if self.cuisine == "" and len(self.ingredients) == 0:
      return self.get_random_question_for_cuisine_and_ingredients()
    if self.cuisine == "" and len(self.ingredients) != 0:
      return self.get_random_question_for_cuisine()
    if self.cuisine != "" and len(self.ingredients) == 0:
      return self.get_random_question_for_ingredients()

  def get_random_greetings(self):
    return random.sample(self.greetings, 1)[0]

  def randomize_apology_response(self):
    apologies = set(
        [
            "Sorry, I don't understand. Try again please.",
            "My apologies, I am having trouble understanding you. Please try rephrasing.",
            "Sorry, I am having trouble understanding. Please try again.",
            "Sorry, I didn't quiet understand what you said. Please try again.",
            "Pardon? Unfortunately I didn't catch that. Please try again.",
        ]
    )
    return random.sample(apologies, 1)[0]

  def check_cuisine(self, text: str) -> bool:
    return any(self.get_cuisine(text))

  def is_ingredient_or_cuisine(self, text: str) -> bool:
    return self.check_ingredient(text) or self.check_cuisine(text)

  def initial_msg(self):
    return f"Hello there! I am Foodie. I can suggest recipes - Ask me any cuisine that you would like to eat today or you can tell me what ingredients you have and I can suggest recipes based on them. Let's get cooking!"

  def start(self) -> None:
    keep_alive = True
    resp = self.initial_msg()
    self.bot_print(resp)
    # resp = ""
    while keep_alive:
      ip: str = input(f"{self.user} ==> ")
      resp = self.chat(ip)
      self.bot_print(resp)
      if resp == "Good Bye.":
        keep_alive = False

  def chat(self, ip: str):
    original_text = ip
    ip = ip.lower()
    resp = ""
    if self.set_person_if_present(original_text):
      # Greetings with name
      resp = f"{self.get_random_greetings().capitalize()} {self.user} 😃 \n"

    # if ip in self.greetings:
    elif any(word in word_tokenize(ip) for word in self.greetings):
      resp = f"{self.get_random_greetings().capitalize()} \n"

    if self.is_ingredient_or_cuisine(ip):
      # check if ingredient add to ingredient
      if self.check_ingredient(ip):
        ing = self.get_ingredient(ip)
        self.ingredients.update(ing)
        if resp != "":
          resp += "</br>"
        resp += "Added ingredients: " + " ".join(ing)

      # check if cuisine update the cuisine
      if self.check_cuisine(ip):
        self.cuisine = self.get_cuisine(ip)[-1]
        if resp != "":
          resp += "</br>"
        resp += "Added cuisine: " + self.cuisine
        resp += "\n"

    if ip.lower() in [
        "exit",
        "close",
        "stop",
        "bye",
        "see you",
        "that's all",
        "that is all",
    ]:
      resp = "Good Bye."

    if "recipe" in ip.lower() or self.cuisineCtr > 0:
      self.cuisineCtr = self.cuisineCtr + 1
      if resp != "":
        resp += "</br>"
      if (
          self.cuisine == "" or len(self.ingredients) == 0
      ) and self.cuisineCtr < random.randrange(2, 4):
        resp += self.check_cuisine_and_ingredients_and_return_reponse()
        # ip: str = input(f"{self.user} ==> ")
        # if ip == "yes":
        #     print("Which cuisine would you like?")
        #     ip: str = input(f"{self.user} ==> ")
      else:
        resp += "Here are few suggestions: </br>"
        if self.cuisine == "":
          self.cuisine = self.get_random_cuisine()
        recipes = get_similar_recipes(self.ingredients, self.cuisine)
        sep = "\n\n"
        i = 0
        for index, row in recipes.iterrows():
          i += 1
          title = str(i) + ". " + "Title: " + row["title"]
          ingredients = ""
          list_ing = (
              row["ingredients"]
              .replace("ADVERTISEMENT", "")
              .strip("][")
              .split(", ")
          )
          for ingredient in list_ing:
            ingredients += ingredient.replace("'", "") + "\n"
          ingredients = "Ingredients: " + "\n" + ingredients
          instructions = "Instruction: " + "\n" + row["instructions"]

          resp += title + sep + ingredients + instructions + "</br>"
        resp = resp.strip("</br>")
        self.ingredients = set([])
        self.cuisine = ""
        self.cuisineCtr = 0

    if resp == "":
      resp = self.randomize_apology_response()
    return resp

  def bot_print(self, resp: str) -> None:
    resp = resp.strip("</br>")
    resp = resp.strip("\n")
    resp += f" <== {self.name}"
    print(resp)
    for line in resp.split("\n"):
      print(f"{line:>70}")


if __name__ == "__main__":
  print(f"{' Starting chatbot ':=^50}")
  cb = ChatBot("foodie")
  cb.start()
