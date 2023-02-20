import pickle
from ngrams import Ngrams, get_bigram_file, get_unigram_file

english_training = "data/LangId.train.English"
french_training = "data/LangId.train.French"
italian_training = "data/LangId.train.Italian"

training_data = [english_training, french_training, italian_training]

test_data = "data/LangId.test"


def main() -> None:
  """
    creates training files for different languages or evaluates training data accuracy
  """

  print(f"\n{' Choose one of the option ':=^50}")
  print("1. Create Model")
  print("2. Evaluate Model")

  val = int(input("Enter a number: "))
  print()

  if (val == 1):
    create_training_data()
  elif (val == 2):
    evaluate()
  else:
    print("Please provide correct input")


def create_training_data() -> None:
  ng = Ngrams()

  for f in training_data:
    lang = f.split(".")[-1].lower()
    print("Creating training data for " + lang)

    unigram_dict, bigram_dict = ng.create_ngrams(f)

    with open(get_unigram_file(lang), 'wb') as f:
      pickle.dump(unigram_dict, f)

    with open(get_bigram_file(lang), 'wb') as f:
      pickle.dump(bigram_dict, f)

    print("Training data created for " + lang)


def evaluate() -> None:
  ng = Ngrams()
  ng.evaluate(test_data)


if __name__ == "__main__":
  main()
