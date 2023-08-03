from typing import Sized


def ensure_len(some: Sized) -> Sized:
    assert len(some), f'{some} given'
    return some
