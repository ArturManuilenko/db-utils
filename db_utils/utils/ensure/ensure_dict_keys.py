from typing import TypeVar, Dict, Iterable

T = TypeVar('T')
T2 = TypeVar('T2')


def ensure_dict_keys(some_dict: Dict[T, T2], keys: Iterable[T]) -> Dict[T, T2]:
    assert isinstance(some_dict, dict)
    for k in keys:
        assert k in some_dict, f'key "{k}" was not found in dict'
    return some_dict
