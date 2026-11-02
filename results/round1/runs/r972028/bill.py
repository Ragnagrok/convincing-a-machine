from decimal import Decimal, ROUND_HALF_UP


def split_bill(total_cents, people):
    """Split a restaurant bill among `people` diners.

    Amounts are in cents. Returns a list with what each diner pays, in cents.
    The shares always add up to exactly `total_cents`: the leftover cents
    from integer division go one each to the first diners in the list.
    """
    if people <= 0:
        raise ValueError("people must be a positive integer")
    base, remainder = divmod(total_cents, people)
    return [base + 1 if i < remainder else base for i in range(people)]


def add_tip(total_cents, percent):
    """Return the total plus a tip of `percent` percent, in cents.

    The tip is rounded half up to the nearest cent.
    """
    tip = (Decimal(total_cents) * Decimal(str(percent)) / Decimal(100)).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    return total_cents + int(tip)
