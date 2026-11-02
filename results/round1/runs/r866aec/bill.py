from fractions import Fraction


def _check_int(name, value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} debe ser int (centavos), no {type(value).__name__}")


def split_bill(total_cents, people):
    """Split a restaurant bill among `people` diners.

    Returns a list with what each diner pays, in cents. Amounts are integers;
    the leftover cents from integer division go one each to the first diners,
    so the shares always add up to exactly `total_cents`.
    """
    _check_int("total_cents", total_cents)
    _check_int("people", people)
    if total_cents < 0:
        raise ValueError("total_cents no puede ser negativo")
    if people < 1:
        raise ValueError("people debe ser al menos 1")

    base, remainder = divmod(total_cents, people)
    return [base + 1 if i < remainder else base for i in range(people)]


def add_tip(total_cents, percent):
    """Return the total plus a tip of `percent` percent, in cents.

    `percent` may be an int, Fraction or Decimal (never a float). The tip is
    rounded half up to the nearest cent.
    """
    _check_int("total_cents", total_cents)
    if isinstance(percent, float):
        raise TypeError("percent no puede ser float; usá int, Fraction o Decimal")
    if total_cents < 0:
        raise ValueError("total_cents no puede ser negativo")
    if percent < 0:
        raise ValueError("percent no puede ser negativo")

    exact_tip = Fraction(total_cents) * Fraction(percent) / 100
    tip = int(exact_tip + Fraction(1, 2))  # round half up, exact
    return total_cents + tip
