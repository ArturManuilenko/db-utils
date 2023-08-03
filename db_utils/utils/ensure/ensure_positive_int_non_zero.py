def ensure_positive_int_non_zero(some: int) -> int:
    assert isinstance(some, int), f'{type(some).__name__} given'
    assert some > 0, f"{some} given"
    return some
