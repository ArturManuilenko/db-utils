from lib.ensure.ensure_int import ensure_int


def ensure_int_positive(some: int) -> int:
    ensure_int(some)
    assert some >= 0, f'{some} given'
    return some


def ensure_int_positive_not_zero(some: int) -> int:
    ensure_int(some)
    assert some > 0, f'{some} given'
    return some
