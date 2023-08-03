from urllib.parse import urlparse


def ensure_url_with_scheme_and_netloc(some: str) -> str:
    assert isinstance(some, str), f'{type(some).__name__} given'
    assert len(some)

    url_r = urlparse(some)

    assert len(url_r.scheme)
    assert len(url_r.netloc)

    return some
