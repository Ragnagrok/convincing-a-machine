"""Bill helpers. All amounts are integer cents: floats lose cents when operated on."""

from decimal import Decimal, ROUND_HALF_UP


def _check_cents(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int number of cents, got {value!r}")


def split_bill(total_cents, people):
    """Split a restaurant bill among `people` diners.

    Returns a list with what each diner pays, in integer cents. The shares
    always sum exactly to `total_cents`: the remainder cents left over from
    the integer division are given one at a time to the first diners, so the
    bank reconciliation closes to the cent.
    """
    _check_cents(total_cents, "total_cents")
    _check_cents(people, "people")
    if people < 1:
        raise ValueError("people must be at least 1")
    if total_cents < 0:
        raise ValueError("total_cents must not be negative")

    base, remainder = divmod(total_cents, people)
    return [base + 1 if i < remainder else base for i in range(people)]


def add_tip(total_cents, percent):
    """Return the total plus a tip of `percent` percent, in integer cents.

    The tip is computed in exact decimal arithmetic and rounded half up to
    the nearest cent. `percent` may be an int or a decimal number such as 12.5.
    """
    _check_cents(total_cents, "total_cents")
    if isinstance(percent, bool) or not isinstance(percent, (int, float, str, Decimal)):
        raise TypeError(f"percent must be a number, got {percent!r}")
    if total_cents < 0:
        raise ValueError("total_cents must not be negative")

    rate = Decimal(str(percent))
    if rate < 0:
        raise ValueError("percent must not be negative")

    tip = (Decimal(total_cents) * rate / Decimal(100)).quantize(
        Decimal(1), rounding=ROUND_HALF_UP
    )
    return total_cents + int(tip)
