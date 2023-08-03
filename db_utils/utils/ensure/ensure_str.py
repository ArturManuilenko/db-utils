def ensure_str(some: str) -> str:
    assert isinstance(some, str), f'{type(some).__name__} given'
    return some
