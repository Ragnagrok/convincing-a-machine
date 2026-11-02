import math


def shipping_cost(weight_kg: float) -> int:
    """Shipping cost in cents. Partial kilos are charged as a whole kilo."""
    kilos = math.ceil(weight_kg)
    if kilos <= 1:
        return 500
    return 500 + 200 * (kilos - 1)
