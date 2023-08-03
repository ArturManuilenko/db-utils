from typing import TypeVar, Dict, Set

T = TypeVar('T')
T2 = TypeVar('T2')


def ensure_dict_keys_strict(some_dict: Dict[T, T2], keys: Set[T]) -> Dict[T, T2]:
    assert isinstance(some_dict, dict)
    assert isinstance(keys, set)
    dict_keys = set(some_dict.keys())
    assert dict_keys == keys, f'invalid keys set. ' \
                              f'{f"dict has unsupported keys {list(dict_keys - keys)}." if len(dict_keys - keys) else ""}' \
                              f'{f"dict no keys {list(keys - dict_keys)}." if len(keys - dict_keys) else ""}'
    return some_dict
