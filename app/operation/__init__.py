"""
Arithmetic operations module.

This module provides basic mathematical operations following functional programming principles.
Demonstrates both LBYL (Look Before You Leap) and EAFP (Easier to Ask Forgiveness than Permission).
"""


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    # LBYL approach - Look Before You Leap
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b