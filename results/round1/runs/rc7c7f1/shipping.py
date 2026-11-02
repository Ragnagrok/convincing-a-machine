import math


def shipping_cost(weight_kg: float) -> int:
    """Shipping cost in cents. Partial kilos are charged as a full kilo."""
    billable_kg = math.ceil(weight_kg)
    if billable_kg <= 1:
        return 500
    return 500 + 200 * (billable_kg - 1)
