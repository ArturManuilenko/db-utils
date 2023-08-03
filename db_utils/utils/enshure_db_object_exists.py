from typing import Optional
from db_utils.modules.db import db
from sqlalchemy.orm.exc import NoResultFound as NoResultFoundError


def enshure_db_object_exists(
    model: db.Model,
    instance: Optional[db.Model]
) -> db.Model:
    if instance is None:
        raise NoResultFoundError(f"{model.__name__} not found")
    return instance
