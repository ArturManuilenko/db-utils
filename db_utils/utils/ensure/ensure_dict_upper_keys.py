from typing import Dict, Any


def ensure_dict_upper_keys(some_dict: Dict[str, Any]) -> Dict[str, Any]:
    assert isinstance(some_dict, dict), f'{type(some_dict).__name__} given'
    for k in some_dict.keys():
        assert isinstance(k, str), f'{type(k).__name__} given'
        assert k.upper() == k, f'"{k}" given'
    return some_dict
