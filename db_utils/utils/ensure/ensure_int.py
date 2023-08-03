def ensure_int(some: int) -> int:
    assert isinstance(some, int), f'{type(some).__name__} given'
    return some
