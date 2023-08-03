def ensure_float(some: float) -> float:
    assert isinstance(some, float), f'{type(some).__name__} given'
    return some
