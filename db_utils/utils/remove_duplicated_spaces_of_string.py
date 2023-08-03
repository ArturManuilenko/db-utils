def remove_duplicated_spaces_of_string(value: str) -> str:
    assert isinstance(value, str), f'{type(value).__name__} given'
    return " ".join(value.split())
