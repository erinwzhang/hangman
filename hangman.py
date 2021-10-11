# Problem Set 2, hangman.py
# Name: Erin Zhang
# Collaborators: N/A
# Sources: https://www.w3schools.com/python/ref_string_replace.asp, https://careerkarma.com/blog/python-print-without-new-line/
# Time spent: 1:30

import random
import string

# -----------------------------------
# HELPER CODE
# -----------------------------------

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    returns: list, a list of valid words. Words are strings of lowercase letters.    
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

# -----------------------------------
# END OF HELPER CODE
# -----------------------------------


# Load the list of words to be accessed from anywhere in the program
wordlist = load_words()

def has_player_won(secret_word, letters_guessed):
    '''
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: boolean, True if all the letters of secret_word are in letters_guessed,
        False otherwise
    '''
    for i in range(len(secret_word)):
        if secret_word[i] not in letters_guessed:
            return False
    return True


def get_word_progress(secret_word, letters_guessed):
    '''
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters and plus signs (+) that represents
        which letters in secret_word have not been guessed so far
    '''
    progress = ""
    for i in range(len(secret_word)):
        if secret_word[i] in letters_guessed:
            progress += secret_word[i]
        else:
            progress += '+'
    return progress


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters that represents which
      letters have not yet been guessed. The letters should be returned in
      alphabetical order
    '''
    alphabet = string.ascii_lowercase
    for i in letters_guessed:
        alphabet = alphabet.replace(i, "")
    return alphabet
    

def reveal_letter(secret_word, available_letters):
    choose_from = ""
    for i in range(len(secret_word)):
        if secret_word[i] in available_letters:
            choose_from += secret_word[i]
    new = random.randint(0, len(choose_from) - 1)
    revealed_letter = choose_from[new]
    return revealed_letter
    

def hangman(secret_word, with_help):
    '''
    secret_word: string, the secret word to guess.
    with_help: boolean, this enables help functionality if true.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses they start with.

    * The user should start with 10 guesses.

    * Before each round, you should display to the user how many guesses
      they have left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a single letter (or help character '!'
      for with_help functionality)

    * If the user inputs an incorrect consonant, then the user loses ONE guess,
      while if the user inputs an incorrect vowel (a, e, i, o, u),
      then the user loses TWO guesses.

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    -----------------------------------
    with_help functionality
    -----------------------------------
    * If the guess is the symbol !, you should reveal to the user one of the
      letters missing from the word at the cost of 3 guesses. If the user does
      not have 3 guesses remaining, print a warning message. Otherwise, add
      this letter to their guessed word and continue playing normally.

    Follows the other limitations detailed in the problem write-up.
    '''
    num_guesses = 10
    letters_guessed = []
    print(secret_word)
    print(f"Welcome to Hangman!\nI am thinking of a word that is {len(secret_word)} letters long.")
    
    while num_guesses > 0 and not has_player_won(secret_word, letters_guessed):
        print(f"--------------\nYou have {num_guesses} guesses left.")
        print("Available letters: " + get_available_letters(letters_guessed), end=(""))
        guess = input("Please guess a letter: ")
        if not guess.isalpha() and guess != "!" or len(guess) != 1:
            if (with_help and guess != "!") or (not with_help):
                print("Oops! That is not a valid letter. Please input a letter from the alphabet: " + get_word_progress(secret_word, letters_guessed))
        elif with_help and guess == "!":
            if num_guesses < 3:
                print("Oops! Not enough guesses left: " + get_word_progress(secret_word, letters_guessed))
            else:
                num_guesses -= 3
                letter_revealed = reveal_letter(secret_word, get_available_letters(letters_guessed))
                letters_guessed.append(letter_revealed)
                print("Letter revealed: " + letter_revealed)
                print(get_word_progress(secret_word, letters_guessed))
        else:
            guess = guess.lower()
            if guess in letters_guessed:
                print("Oops! You've already guessed that letter: " + get_word_progress(secret_word, letters_guessed))
            elif guess not in secret_word:
                vowels = "aeiou"
                if guess in vowels:
                    num_guesses -= 2
                else:
                    num_guesses -= 1
                letters_guessed.append(guess)
                print("Oops! That letter is not in my word: " + get_word_progress(secret_word, letters_guessed))
            else:
                letters_guessed.append(guess)
                print("Good guess: " + get_word_progress(secret_word, letters_guessed))

    if "+" in get_word_progress(secret_word, letters_guessed):
        print("--------------")
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")
    else:
        count = 0
        for i in letters_guessed:
            if i in secret_word:
                count += 1
        total_score = (4 * count * num_guesses) + (2 * len(secret_word))
        print("--------------")
        print(f"Congratulations, you won!\nYour total score for this game is: {total_score}")

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the lines to test

if __name__ == "__main__":
    # To test your game, uncomment the following two lines.
    secret_word = choose_word(load_words())
    with_help = True
    hangman(secret_word, with_help)

    # After you complete with_help functionality, change with_help to True
    # and try entering "!" as a guess!

    ###############

    # SUBMISSION INSTRUCTIONS
    # -----------------------
    # It doesn't matter if the lines above are commented in or not
    # when you submit your pset. However, please run ps2_student_tester.py
    # one more time before submitting to make sure all the tests pass.
    pass