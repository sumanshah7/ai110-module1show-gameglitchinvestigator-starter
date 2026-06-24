# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** A Streamlit number-guessing game: the app picks a secret number inside a range that depends on the chosen difficulty (Easy 1–20, Normal 1–100, Hard 1–50), and the player has a limited number of attempts to guess it. After each guess the game gives a "Too High" / "Too Low" hint and updates a running score.
- [x] **Detail which bugs you found.**
  1. **Secret out of range** — the secret was generated once and never regenerated when the difficulty changed, so an Easy/Hard game could hold a Normal-range secret.
  2. **Backwards hints** — "Too High" told you to go HIGHER (and the secret was being coerced to a string on some attempts, so numbers were compared as text).
  3. **Dead Submit button** — "New Game" reset attempts and the secret but not `status`, so after a win/loss the next rerun hit `st.stop()` and Submit did nothing until a full page refresh.
- [x] **Explain what fixes you applied.** Regenerated the secret whenever the game loads or difficulty changes; corrected the hint directions and removed the `str()` coercion so comparisons stay integer; reset `status` (and score/history) in the New Game handler. Core logic was refactored out of `app.py` into `logic_utils.py` so it could be unit-tested.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (range 1–100, secret = 26):

1. User enters a guess of `10` → game returns "📈 Too low — go HIGHER!"
2. User enters a guess of `60` → game returns "📉 Too high — go LOWER!"
3. User enters a guess of `30` → game returns "📉 Too high — go LOWER!"
4. Score updates after each guess and the "Attempts left" counter decreases.
5. User enters a guess of `26` → game returns "🎉 Correct!", shows balloons, reports the final score, and locks the board.
6. User clicks **New Game 🔁** → a fresh secret is drawn and the Submit button responds immediately (no page refresh needed).

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest -q
.....................                                                    [100%]
21 passed in 0.02s
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
