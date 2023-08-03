from contextlib import contextmanager
from typing import Any

from db_utils.modules.db import db

transaction_context = False


@contextmanager
def transaction_commit() -> Any:
    global transaction_context
    try:
        transaction_context = True
        yield
        db.session.commit()
        transaction_context = False
    except Exception:
        db.session.rollback()
        raise
