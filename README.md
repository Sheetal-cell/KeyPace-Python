🖥️ KeyPace — Your Ultimate Typing Speed & Accuracy Trainer ⚡
Welcome to KeyPace, a fun and colorful terminal-based typing test game designed to help you boost your typing speed and accuracy! Whether you’re a beginner or looking to sharpen your keyboard skills, KeyPace makes practicing engaging and rewarding — with real-time results, multiple sentences, and a competitive leaderboard to track your progress.

🎯 Features
🔸Multiple sentences to practice — Choose how many sentences you want to type.
🔸Real-time typing speed calculation — Measures your Words Per Minute (WPM) precisely.
🔸Accuracy scoring — See how many words you got right in each sentence.
🔸Colorful and user-friendly terminal interface — Powered by Colorama.
🔸Persistent leaderboard — Save your scores and compare with others’ top performances.
🔸Easy menu navigation — Start tests, view leaderboard, or exit with simple inputs.

💻 How to Use
👍Clone or download the repository

git clone https://github.com/yourusername/keypace.git
cd keypace

👍Install the required dependency

🔸KeyPace uses Colorama for colored text output. Install it with:
pip install colorama

👍Run the program

python keypace.py

👍Follow on-screen instructions

🔸Select Start Typing Test to choose the number of sentences and begin typing.
🔸After each sentence, your time, speed, and accuracy will be displayed.
🔸After all sentences, see your average results and save your score to the leaderboard.
🔸View the leaderboard anytime to check top scores.

📈 How It Works — Behind the Scenes
🔸Random sentences are selected from a predefined list for you to type.
🔸Your input is timed, and WPM is calculated as (words / time) * 60.
🔸Accuracy is calculated by comparing typed words with the original sentence.
🔸Your average speed and accuracy are saved to a leaderboard file with your name and timestamp.
🔸Leaderboard displays the top 5 scores sorted by highest WPM.