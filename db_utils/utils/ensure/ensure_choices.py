from typing import TypeVar, Set, List, Tuple, Union


T = TypeVar('T')


def ensure_choices(some: T, choices: Union[Set[T], List[T], Tuple[T, ...]]) -> T:
    assert isinstance(choices, (set, tuple, list)), f'{type(choices).__name__} given'
    assert len(choices)
    assert some in choices, f'must be in [{list(choices)}]. {some} given'

    return some
