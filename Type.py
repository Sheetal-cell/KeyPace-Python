import time
import random
from colorama import init, Fore, Style
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# Welcome message
print(Fore.CYAN + "="*60)
print(Fore.MAGENTA + Style.BRIGHT + "             WELCOME TO KEYPACE 🖥️⚡")
print(Fore.YELLOW + "        Type Fast. Type Smart. Beat your best!")
print(Fore.CYAN + "="*60)
time.sleep(1)

# List of sentences
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a versatile programming language.",
    "Practice makes perfect when it comes to typing.",
    "Stay focused and keep improving your pace.",
    "Typing fast is a useful skill for everyone.",
    "The sun sets in the west and rises in the east.",
    "Knowledge is power and enthusiasm pulls the switch.",
    "Never stop exploring new opportunities and ideas.",
    "Challenges make life interesting and rewarding.",
    "Keep calm and code on with Python.",
    "Good habits formed at youth make all the difference.",
    "Typing with speed and accuracy is a valuable asset.",
    "Work smart, stay humble, and hustle hard.",
    "Patience and practice pave the path to perfection.",
    "Every moment is a fresh beginning, make it count."
]

# Ask how many sentences the user wants to type
num_sentences = int(input(Fore.GREEN + "\nHow many sentences would you like to type? "))

total_wpm = 0
total_accuracy = 0

for i in range(num_sentences):
    print(Fore.CYAN + f"\nSentence {i+1} of {num_sentences}:")
    sentence = random.choice(sentences)
    print(Fore.YELLOW + f"\nType the following:\n\"{sentence}\"")

    start_time = time.time()
    user_input = input(Fore.WHITE + "\nStart typing here: ")
    end_time = time.time()

    time_taken = end_time - start_time
    words = len(sentence.split())
    wpm = (words / time_taken) * 60

    correct_words = len(set(user_input.split()) & set(sentence.split()))
    accuracy = (correct_words / words) * 100

    print(Fore.MAGENTA + "\n----- Result for this sentence -----")
    print(Fore.GREEN + f"Time Taken: {round(time_taken, 2)} seconds")
    print(Fore.GREEN + f"Typing Speed: {round(wpm, 2)} WPM")
    print(Fore.GREEN + f"Accuracy: {round(accuracy, 2)}%")
    print(Fore.MAGENTA + "------------------------------------")

    total_wpm += wpm
    total_accuracy += accuracy

# Final average results
avg_wpm = total_wpm / num_sentences
avg_accuracy = total_accuracy / num_sentences

print(Fore.CYAN + "\n===============================")
print(Fore.MAGENTA + Style.BRIGHT + "         FINAL RESULTS          ")
print(Fore.CYAN + "===============================")
print(Fore.YELLOW + f"Average Typing Speed: {round(avg_wpm, 2)} WPM")
print(Fore.YELLOW + f"Average Accuracy: {round(avg_accuracy, 2)}%")
print(Fore.CYAN + "===============================")

# Save to leaderboard
name = input(Fore.GREEN + "\nEnter your name to save your score to the leaderboard: ")
date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("leaderboard.txt", "a") as file:
    file.write(f"{name} | {date_now} | {round(avg_wpm,2)} WPM | {round(avg_accuracy,2)}% Accuracy\n")

print(Fore.GREEN + "\nYour score has been saved to the leaderboard! 📃✨")

print(Fore.CYAN + "\nThanks for playing KeyPace! 🖥️⚡ Keep practicing and level up!\n")
