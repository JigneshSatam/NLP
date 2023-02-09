from random import choice


class GuessingGame:
  def __init__(self, words: list[str]) -> None:
    self.words = words
    self.points: int = 5

  def start(self, welcome_msg: bool = False) -> None:
    if welcome_msg:
      print_msg("Let's play a word guessing game!")

    print(f"\nCurrent score: {self.points}")

    stop: bool = False
    while not stop:
      self.initialize()
      stop = self.play()
      if not stop:
        print("Guess another word")

  def initialize(self) -> None:
    # Randomly choose a word
    self.word = choice(self.words)

    # Initialize guessed_letters to with "_" for number for letters in the choosen word
    self.guessed_leters: list[str] = ["_" for _ in self.word]

  def play(self) -> None:

    while self.points > 0:
      self.display_word()

      # Take user input
      ip: str = input("Guess a letter: ")

      # Stop if user input is "!"
      if ip == "!":
        break

      # Current Letter Socre is -1
      score = -1

      for i, l in enumerate(self.word):
        if l == ip:
          # Check if new letter is guessed
          if self.guessed_leters[i] == "_":
            # Current Letter Socre is +1 if new letter is guessed
            score = 1
            self.guessed_leters[i] = l
          else:
            # Current Letter Socre is 0 if existing letter is guessed
            score = 0

      # Update points
      self.points += score

      # if new letter is guessed
      if score == 1:
        print(f"Right!", end=" ")
      # if existing letter is guessed
      elif score == 0:
        print(f"Already guessed!", end=" ")
      # if wrong letter is guessed
      else:
        print(f"Sorry, guess again.", end=" ")

      print(f"Score is {self.points}")
      print()

      # Check if all the letters are guessed and start the game
      if "".join(self.guessed_leters) == self.word:
        self.display_word()
        print_msg("You solved it!")
        return False

    return True

  def display_word(self) -> None:
    for l in self.guessed_leters:
      print(l, end=' ')
    print()


def print_msg(msg: str) -> None:
  print(f"\n{'':=^50}")
  print("{:=^50}".format(f" {msg} "))
  print(f"{'':=^50}")
