import argparse
from guessing_game import GuessingGame, print_msg
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def load() -> None:
  """
  loads the data from the input file provided.

  Exits if no argument for input file is provided.
  """

  parser = argparse.ArgumentParser(
      usage="main.py [-h] -i INPUT \nRequires text file as an input to create the guessing game")
  parser.add_argument(
      '-i', '--input', help='Input file location', required=True)
  args = parser.parse_args()
  input_file = args.input

  print_msg("Document Summary")

  raw_text = ""
  with open(input_file, "r") as f:
    raw_text = f.read()

  tokens, nouns = preprocess(raw_text)

  # Print lexical diversity
  calculate_lexical_diversity(tokens)

  # makes a dictionary of noun and its count in tokens
  nouns_dict = {n: tokens.count(n) for n in nouns}

  # get a sorted list of tuples: (noun, count)
  count_sorted_nouns = sorted(
      nouns_dict.items(), key=lambda x: x[1], reverse=True)

  game_words = [w[0] for w in count_sorted_nouns[:50]]

  gg = GuessingGame(game_words)
  gg.start(welcome_msg=True)


def calculate_lexical_diversity(tokens: list[str]) -> None:
  """
  calculate_lexical_diversity

  calculates lexical diversity from the tokens and prints it
  """
  lexical_diversity = len(set(tokens)) / len(tokens)

  print(f"\nLexical diversity: {lexical_diversity:.2f}")


def preprocess(raw_text: str) -> tuple[list[str], list[str]]:
  """
  preprocesses the raw text and returns tokens and nouns by applying following operations.

  Operations for tokens generation:
  1. Remove non-alpha tokens
  2. Keep words having length greater than 5
  3. Convert to lower case
  4. Remove stopwords

  Operations for nouns generation:
  1. lemmatize tokens
  2. Removing duplicates
  3. POS tagging the unique lemmas
  4. Filter nouns from tagged lemmas

  :param raw_text: string which is to be processed
  :return: list of tokens and list of nouns
  """
  long_lower_alpha_tokens = [t.lower()
                             for t in word_tokenize(raw_text) if t.isalpha() and
                             len(t) > 5]

  english_stopwords = set(stopwords.words('english'))
  non_stopwords_tokens = [
      t for t in long_lower_alpha_tokens if (t not in english_stopwords)]

  wnl = WordNetLemmatizer()
  lemmas = [wnl.lemmatize(t) for t in non_stopwords_tokens]
  lemmas_unique = list(set(lemmas))

  lemmas_tags = pos_tag(lemmas_unique)

  print("\nFirst 20 tagged unique lemmas:\n", lemmas_tags[:20])

  nouns = [t[0] for t in lemmas_tags if t[1].startswith("NN")]

  print("\nNumber of tokens", len(non_stopwords_tokens))

  print("\nNumber of nouns", len(nouns))

  return non_stopwords_tokens, nouns


if __name__ == "__main__":
  load()
