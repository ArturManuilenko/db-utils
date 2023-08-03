from typing import List, Type, TypeVar

T = TypeVar('T')


def ensure_list_of(value: List[T], item_kind: Type[T]) -> List[T]:
    assert isinstance(value, list), f'{type(value).__name__} given'
    for item in value:
        assert isinstance(item, item_kind), f'{type(value).__name__}'

    return value
