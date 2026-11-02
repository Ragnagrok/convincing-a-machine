def shipping_cost(weight_kg: float) -> int:
    """Shipping cost in cents."""
    if weight_kg <= 1:
        return 500
    return 500 + 200 * int(weight_kg - 1)
