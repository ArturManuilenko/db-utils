from typing import TypeVar, Dict, Set

T = TypeVar('T')
T2 = TypeVar('T2')


def ensure_dict_keys_choice(some_dict: Dict[T, T2], keys: Set[T]) -> Dict[T, T2]:
    assert isinstance(some_dict, dict)
    assert isinstance(keys, set)
    dict_keys = set(some_dict.keys())
    assert not len(dict_keys - keys), f"dict has unsupported keys {list(dict_keys - keys)}."
    return some_dict
