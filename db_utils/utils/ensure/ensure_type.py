from typing import TypeVar, Type

T = TypeVar('T')


def ensure_type(value: T, value_type: Type[T]) -> T:
    assert isinstance(value, value_type), f'{type(value).__name__} given, expected {value_type}'
    return value
