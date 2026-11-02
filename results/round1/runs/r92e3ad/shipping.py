import math


def shipping_cost(weight_kg: float) -> int:
    """Shipping cost in cents. Partial kilos are charged as a full kilo."""
    kilos = max(1, math.ceil(weight_kg))
    return 500 + 200 * (kilos - 1)
