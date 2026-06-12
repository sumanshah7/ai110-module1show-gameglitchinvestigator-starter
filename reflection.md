# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The game look normal for first game but during my second and third attemp it was giving wrong output.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  1. The random secret number ignored the difficulty range — even though each difficulty sets a limit, the game generated a number outside it.
  2. The hints were wrong/backwards, so the "go higher / go lower" feedback led me in the wrong direction.
  3. After clicking "New Game" the screen reset, but the Submit button stopped responding until I refreshed the whole page.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
|------------|-------------------|-------------------|------------------------|
| Difficulty set to Hard (1–50) | Secret within 1–50 | Secret out of range | `The secret was 26. Score: -5`  |
| Guess of 3 (secret is higher) | "Go HIGHER" hint   | "Go LOWER" hint shown | none |
| Click New Game, then Submit   | Submit accepts new guess | Submit does nothing until refresh | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude (Claude Code) as my main AI teammate while debugging this project. I described the three glitches I saw in plain language and it traced each one back to the exact line in `app.py`. A correct suggestion was that the "New Game" button never reset the `status` variable, which is why Submit stopped responding until I refreshed — I verified this by reading the code and seeing that `st.stop()` fired whenever status was still "won" or "lost". The AI did not give me an incorrect or misleading suggestion on this project; its explanations matched what I saw in the code, and I confirmed each fix by reproducing the bug and running my tests.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed by reproducing the exact steps that broke it and checking the new behavior, then backing that up with automated tests. I moved the logic into `logic_utils.py` and wrote `test_case.py`, then ran `pytest test_case.py -v` and got 21 passing tests. One useful test drew 1,000 random secrets for each difficulty and asserted every one stayed inside that difficulty's range, which proved the out-of-range bug was gone. Another test replayed my exact 10 → 5 → 3 → 4 guess sequence against the secret 26 and confirmed the hint no longer flips direction. AI helped me design these tests by pointing out edge cases I had not thought of, like empty input, decimals, and unknown difficulty values.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I would tell a friend that Streamlit re-runs the entire script from top to bottom every single time you click a button or change an input — it does not just update one piece. Because of that, any normal variable resets on every click, so it would forget the secret number and your score. `st.session_state` is like a small backpack that survives those reruns, so things you store in it (the secret, attempts, score, status) stay remembered between clicks. The big lesson was that bugs like the dead Submit button came from session state not being reset properly, not from the button itself.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is writing automated tests for the logic instead of only clicking through the app by hand, because the tests caught problems faster and gave me confidence the fix actually held. Next time I would separate the logic from the UI earlier (like putting functions in `logic_utils.py` from the start) so the code is testable before I even hit a bug. This project changed how I think about AI-generated code: it can look polished and "production-ready" while still hiding real bugs, so I now treat AI output as a draft I have to read, question, and test rather than trust blindly.
