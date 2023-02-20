
import pickle
from nltk import word_tokenize
from nltk.util import ngrams
from decimal import Decimal


class Ngrams:

  def create_ngrams(self, training_file: str) -> list[dict[tuple[str], int]]:
    """
      Create unigram and bigrams dictionary from the training file

      params: training_file input for training

      return: unigram dictionary and bigrams dictionary
    """

    raw_text = ""
    with open(training_file, "r") as f:
      raw_text = f.read()

    unigrams, bigrams = self.preprocess_data(raw_text)
    unigrams_set = set(unigrams)
    bigrams_set = set(bigrams)
    unigram_dict = {t: unigrams.count(t) for t in unigrams_set}
    bigram_dict = {b: bigrams.count(b) for b in bigrams_set}

    # print(unigram_dict)
    # print(bigram_dict)
    return [unigram_dict, bigram_dict]

  def preprocess_data(self, text: str) -> list[list[tuple[str]]]:
    # tokens_before = word_tokenize(text)
    # print(len(tokens_before))
    # text = text.replace("\n", " ")

    tokens = [t.lower() for t in word_tokenize(text)]
    # print(len(tokens))
    unigrams = list(ngrams(tokens, 1))
    bigrams = list(ngrams(tokens, 2))

    # print(len(unigrams))
    # print(len(bigrams))
    return [unigrams, bigrams]

  def evaluate(self, test_file: str) -> None:
    """
      Create solution for the test file and computes the accuracy with the solution

      params: test_file input for testing
    """

    self.predict_result(test_file)
    self.calculate_accuracy()

  def predict_result(self, test_file: str) -> None:
    """
      Create solution for the test file
    """

    v = 0
    training_data_dict = {}

    for lang in ["english", "french", "italian"]:
      unigram_dict = pickle.load(open(get_unigram_file(lang), 'rb'))
      bigram_dict = pickle.load(open(get_bigram_file(lang), 'rb'))
      training_data_dict[lang] = (unigram_dict, bigram_dict)
      v += len(unigram_dict)

    result = ""
    i = 0

    # line_number = 0
    # print_number = 44

    with open(test_file, "r") as f:

      for line in f.readlines():
        i += 1
        max_prob = Decimal(0)
        max_prob_lang = ""

        # line_number += 1
        # if line_number == print_number:
        #   print(line)

        for lang, data in training_data_dict.items():
          unigram_dict, bigram_dict = data
          prob = Decimal(self.compute_prob(line, unigram_dict, bigram_dict, v))

          # if line_number == print_number:
          #   print("line ", i, ": ", lang, " ", prob)

          if max_prob < prob:
            max_prob = prob
            max_prob_lang = lang

        result += str(i) + " " + max_prob_lang.capitalize() + "\n"

    with open(self.get_result_file(), "w") as f:
      f.write(result)

  def compute_prob(self, text, unigram_dict, bigram_dict, v: int) -> Decimal:
    """
      calculates the probability for the given text

      params: text raw_text for which probability is calculated
      params: unigram_dict training unigrams
      params: bigram_dict training bigrams
      param: v is the vocabulary size in the training data (unique tokens)
    """

    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    # p_gt = 1       # calculate p using a variation of Good-Turing smoothing
    probability = Decimal(1.0)  # calculate p using Laplace smoothing
    # p_log = 0      # add log(p) to prevent underflow

    for bigram in bigrams_test:
      n = bigram_dict[bigram] if bigram in bigram_dict else 0

      # n_gt = bigram_dict[bigram] if bigram in bigram_dict else 1/N
      d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0

      # if d == 0:
      #   p_gt = p_gt * (1 / N)
      # else:
      #   p_gt = p_gt * (n_gt / d)
      probability = Decimal(
          probability * Decimal(Decimal(n + 1) / Decimal(d + v)))
      # p_log = p_log + math.log((n + 1) / (d + V))

    return probability

  def calculate_accuracy(self) -> None:
    """
     Computes the accuracy with the solution
    """

    with open(self.get_result_file(), "r") as f:
      results = f.readlines()

    with open("data/LangId.sol", "r") as f:
      solutions = f.readlines()

    total = len(solutions)
    correct = 0
    incorrect = []
    for i in range(total):
      if solutions[i] == results[i]:
        correct += 1
      else:
        incorrect.append(i+1)

    print(f"{' Evaluation ':=^50}")
    print("Accuracy: ", (correct * 100 / total))
    print("Incorrect lines:", incorrect)

  @staticmethod
  def get_result_file() -> str:
    return "result/output.sol"


def get_unigram_file(lang: str) -> str:
  return "training-data/" + lang + "_unigram.pickle"


def get_bigram_file(lang: str) -> str:
  return "training-data/" + lang + "_bigram.pickle"
