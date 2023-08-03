def ensure_bool(some: bool) -> bool:
    assert isinstance(some, bool), f'{type(some).__name__} given'
    return some
