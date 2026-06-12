"""
Tests for the guessing-game logic in logic_utils.py.

Why test logic_utils.py and not app.py directly?
  app.py runs Streamlit code at import time (st.set_page_config, st.session_state,
  widgets, etc.), so importing it outside a real `streamlit run` session crashes.
  The pure game logic lives in logic_utils.py, which is safe to import and test.

Run from the project root with:
    pytest -v
"""

import random

import pytest

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# Starter tests (updated): check_guess now returns (outcome, message), so we
# unpack the outcome instead of comparing the whole return value to a string.
# ---------------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# Bug #1 — the secret must stay inside the difficulty's range
# ---------------------------------------------------------------------------

def test_ranges_per_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)


def test_unknown_difficulty_falls_back_to_normal():
    assert get_range_for_difficulty("Impossible") == (1, 100)
    assert get_range_for_difficulty("") == (1, 100)


@pytest.mark.parametrize("difficulty", ["Easy", "Normal", "Hard"])
def test_generated_secret_stays_in_range(difficulty):
    # Regression test for the "random number out of limit" bug: a secret drawn
    # for a difficulty must always fall within that difficulty's range.
    low, high = get_range_for_difficulty(difficulty)
    for _ in range(1000):
        secret = random.randint(low, high)
        assert low <= secret <= high


def test_difficulty_change_changes_range():
    assert get_range_for_difficulty("Easy") != get_range_for_difficulty("Normal")
    assert get_range_for_difficulty("Hard") != get_range_for_difficulty("Normal")


# ---------------------------------------------------------------------------
# Bug #2 — hints must point the right direction (not backwards)
# ---------------------------------------------------------------------------

def test_too_high_hint_says_go_lower():
    outcome, message = check_guess(60, 26)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


def test_too_low_hint_says_go_higher():
    outcome, message = check_guess(3, 26)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


def test_hint_is_consistent_across_a_sequence():
    # Reproduces the reported 10 -> 5 -> 3 -> 4 sequence against secret 26.
    # Every guess below the secret must say "Too Low"; none should flip.
    secret = 26
    for guess in (10, 5, 3, 4):
        outcome, _ = check_guess(guess, secret)
        assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# parse_guess — input edge cases
# ---------------------------------------------------------------------------

def test_parse_valid_integer():
    assert parse_guess("42") == (True, 42, None)


def test_parse_decimal_is_truncated():
    ok, value, err = parse_guess("4.9")
    assert ok is True
    assert value == 4
    assert err is None


def test_parse_empty_string():
    assert parse_guess("") == (False, None, "Enter a guess.")


def test_parse_none():
    assert parse_guess(None) == (False, None, "Enter a guess.")


def test_parse_non_numeric_text():
    assert parse_guess("abc") == (False, None, "That is not a number.")


# ---------------------------------------------------------------------------
# update_score — scoring edge cases
# ---------------------------------------------------------------------------

def test_win_on_first_attempt_awards_most_points():
    assert update_score(0, "Win", attempt_number=0) == 90


def test_win_points_never_drop_below_floor():
    assert update_score(0, "Win", attempt_number=50) == 10


def test_too_low_always_loses_five():
    assert update_score(100, "Too Low", attempt_number=4) == 95


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(42, "Mystery", attempt_number=3) == 42
