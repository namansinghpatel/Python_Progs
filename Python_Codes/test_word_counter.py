# Run the program as pytest -sv .\test_word_counter.py

from word_counter import count_words

def test_basic():
    assert count_words("hello world") == 2


def test_leading_spaces():
    assert count_words("   hello world") == 2


def test_multiple_spaces():
    assert count_words("hello   world") == 2


def test_trailing_spaces():
    assert count_words("hello world   ") == 2


def test_empty_string():
    assert count_words("") == 0


def test_only_spaces():
    assert count_words("     ") == 0


def test_single_word():
    assert count_words("python") == 1


def test_multiple_words():
    assert count_words("python is very easy") == 4