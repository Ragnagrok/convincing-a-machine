from fractions import Fraction


def _check_cents(value, name):
    # Montos en centavos: solo enteros (nunca floats, ni siquiera 10.0).
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} debe ser int (centavos), recibido {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} no puede ser negativo")


def split_bill(total_cents, people):
    """Split a restaurant bill among `people` diners.

    Returns a list with the amount in cents each person pays. The amounts
    always sum exactly to `total_cents`: the remainder cents (total % people)
    are distributed one each to the first diners.
    """
    _check_cents(total_cents, "total_cents")
    if isinstance(people, bool) or not isinstance(people, int):
        raise TypeError("people debe ser int")
    if people < 1:
        raise ValueError("people debe ser al menos 1")

    base, remainder = divmod(total_cents, people)
    return [base + 1 if i < remainder else base for i in range(people)]


def add_tip(total_cents, percent):
    """Return the total plus a tip of `percent` percent, in cents.

    `percent` may be an int or a Fraction/Decimal (e.g. 12.5 as Decimal("12.5")),
    never a float. The tip is rounded half up to the nearest cent.
    """
    _check_cents(total_cents, "total_cents")
    if isinstance(percent, (float, bool)):
        raise TypeError("percent no puede ser float ni bool; usá int, Decimal o Fraction")
    try:
        pct = Fraction(percent)
    except (TypeError, ValueError):
        raise TypeError("percent debe ser int, Decimal o Fraction") from None
    if pct < 0:
        raise ValueError("percent no puede ser negativo")

    tip = Fraction(total_cents) * pct / 100
    tip_cents = int(tip + Fraction(1, 2))  # redondeo half-up exacto
    return total_cents + tip_cents
