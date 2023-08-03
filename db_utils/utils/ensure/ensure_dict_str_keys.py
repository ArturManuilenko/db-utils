from typing import Dict, Any


def ensure_dict_str_keys(some_dict: Dict[str, Any]) -> Dict[str, Any]:
    assert isinstance(some_dict, dict), f'{type(some_dict).__name__} given'
    for k in some_dict.keys():
        assert isinstance(k, str), f'{type(k).__name__} given'
    return some_dict
