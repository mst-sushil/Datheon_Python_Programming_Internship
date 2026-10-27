import random

# ASCII stages for wrong attempts (0 to 6 errors)
HANGMAN_PICS = [
    """
     +---+
         |
         |
         |
        ===""",
    """
     +---+
     O   |
         |
         |
        ===""",
    """
     +---+
     O   |
     |   |
         |
        ===""",
    """
     +---+
     O   |
    /|   |
         |
        ===""",
    """
     +---+
     O   |
    /|\\  |
         |
        ===""",
    """
     +---+
     O   |
    /|\\  |
    /    |
        ===""",
    """
     +---+
     O   |
    /|\\  |
    / \\  |
        ==="""
]

# Load words from 'google-10000-english-no-swears.txt' file
try:
    with open("google-10000-english-no-swears.txt", "r", encoding="utf-8") as file:
        # 4 letters ya usse bade words filter karte hain taaki game accha chale
        WORD_LIST = [line.strip().upper() for line in file if line.strip() and len(line.strip()) >= 4]
except FileNotFoundError:
    # Fallback list agar file na mile
    WORD_LIST = ["PYTHON", "PROGRAMMING", "DEVELOPER", "INTERNSHIP", "DATHEON", "CONSOLE"]

def play_hangman():
    word = random.choice(WORD_LIST)
    word_letters = set(word)  # letters in the word
    guessed_letters = set()   # letters guessed by user
    incorrect_guesses = 0
    max_attempts = 6

    print("=" * 40)
    print("   WELCOME TO HANGMAN WORD GAME   ")
    print("=" * 40)

    while incorrect_guesses < max_attempts and len(word_letters) > 0:
        # Display current hangman art
        print(HANGMAN_PICS[incorrect_guesses])
        
        # Display word progress (e.g., P _ T H _ _ )
        word_display = [letter if letter in guessed_letters else '_' for letter in word]
        print("\nWord to guess: ", " ".join(word_display))
        print(f"Guessed letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
        print(f"Remaining Lives: {max_attempts - incorrect_guesses}")

        # Get user input
        user_guess = input("\nGuess a letter: ").upper().strip()

        # Input validation
        if not user_guess.isalpha() or len(user_guess) != 1:
            print("⚠️ Invalid input! Please enter a single alphabetical letter.")
            continue

        # Check for duplicate guess
        if user_guess in guessed_letters:
            print(f"⚠️ You already guessed '{user_guess}'. Try a different letter! (No penalty)")
            continue

        # Add to guessed set
        guessed_letters.add(user_guess)

        # Check if guess is correct
        if user_guess in word_letters:
            word_letters.remove(user_guess)
            print(f"✅ Good job! '{user_guess}' is in the word.")
        else:
            incorrect_guesses += 1
            print(f"❌ Wrong guess! '{user_guess}' is not in the word.")

    # Game over / Victory screens
    print("\n" + "=" * 40)
    if len(word_letters) == 0:
        print(HANGMAN_PICS[incorrect_guesses])
        print(f"🎉 CONGRATULATIONS! You guessed the word: {word}")
    else:
        print(HANGMAN_PICS[max_attempts])
        print(f"❌ GAME OVER! The secret word was: {word}")
    print("=" * 40)

if __name__ == "__main__":
    while True:
        play_hangman()
        again = input("\nDo you want to play again? (y/n): ").lower()
        if again != 'y':
            print("Thanks for playing! Task 1 completed successfully.")
            break
