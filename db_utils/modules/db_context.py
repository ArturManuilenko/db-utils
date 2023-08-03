from functools import wraps
from typing import Any, Callable, Dict

from flask import Flask

from db_utils import transaction_commit


def db_context(app: Flask) -> Callable[[Any], Any]:
    def wrap(fn: Callable[[], Any]) -> Callable[[], Any]:
        @wraps(fn)
        def new_fn() -> Callable[[], Any]:
            with app.app_context():
                return fn()
        return new_fn
    return wrap


def db_context_transaction_commit(app: Flask) -> Callable[[Any], Any]:
    def wrap(fn: Any) -> Callable[[], Any]:
        @wraps(fn)
        def new_fn(*args: Any, **kwargs: Dict[str, Any]) -> Callable[[], Any]:
            with app.app_context():
                with transaction_commit():
                    return fn(*args, **kwargs)
        return new_fn
    return wrap
