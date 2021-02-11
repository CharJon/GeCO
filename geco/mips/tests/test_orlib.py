import pytest
import os
from geco.mips.loading.orlib import *


def test_read_multiline_correct():
    content = b"""1 2 3.5\n 3 2 1\n"""
    with open("temp", "wb") as f:
        f.write(content)

    with open("temp", "rb") as f:
        numbers = read_multiline_numbers(file=f, number_to_read=6)
        assert len(numbers) == 6
        assert list(numbers) == [1, 2, 3.5, 3, 2, 1]

    with open("temp", "rb") as f, pytest.raises(ValueError):
        read_multiline_numbers(f, 5)

    os.unlink("temp")


def test_read_number():
    n_1 = read_number(b"1")
    n_half = read_number(b".5")
    assert isinstance(n_1, int) and n_1 == 1
    assert isinstance(n_half, float) and n_half == 0.5


def test_read_numbers():
    expected_numbers = [1, 2.5, 3]
    numbers = read_numbers(b"  1 2.5 3 \n")
    for read, expected in zip(numbers, expected_numbers):
        assert read == expected
