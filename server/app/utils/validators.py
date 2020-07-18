"""This module provides validators for models data."""


def validate_budget(data):
    """Validate budget input."""
    errors = []

    savings = data.get("savings")
    if savings and not 0 <= savings <= 100:
        errors.append("Savings is out of range.")

    income = data.get("income")
    if income and income < 0:
        errors.append("Income must be positive.")

    return errors
