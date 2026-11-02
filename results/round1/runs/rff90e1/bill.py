from decimal import Decimal, ROUND_HALF_UP


def _check_cents(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer number of cents")
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def split_bill(total_cents, people):
    """Split a restaurant bill among `people` diners.

    Amounts are integer cents. Each diner pays the same base share; the
    leftover cents (total % people) are given one by one to the first
    diners, so the shares always add up exactly to `total_cents`.

    Returns a list with the amount in cents each diner pays.
    """
    _check_cents(total_cents, "total_cents")
    if isinstance(people, bool) or not isinstance(people, int):
        raise TypeError("people must be an integer")
    if people < 1:
        raise ValueError("people must be at least 1")

    base, remainder = divmod(total_cents, people)
    return [base + 1 if i < remainder else base for i in range(people)]


def add_tip(total_cents, percent):
    """Return the total plus a tip of `percent` percent, in integer cents.

    The tip is computed exactly with Decimal and rounded half-up to the
    nearest cent, so no float error creeps into the result.
    """
    _check_cents(total_cents, "total_cents")
    if percent < 0:
        raise ValueError("percent must be non-negative")

    tip = (Decimal(total_cents) * Decimal(str(percent)) / Decimal(100)).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    return total_cents + int(tip)
