from typing import TypeVar, Set

T = TypeVar('T')


def ensure_set(some: Set[T]) -> Set[T]:
    assert isinstance(some, set), f'{type(some).__name__} given'
    return some
