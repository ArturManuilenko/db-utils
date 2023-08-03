from db_utils.modules.db import db
from db_utils.model.base_model import BaseModel
from db_utils.model.base_user_log_model import BaseUserLogModel
from typing import Any, Dict, List, Union


def get_models_template(model: Union[List[db.Model], db.Model]) -> Dict[str, Any]:
    base_user_log_model_columns = BaseUserLogModel.__dict__.keys()
    base_model_columns = BaseModel.__dict__.keys()
    model_columns: Dict[str, Any] = dict()
    for db_model in model:
        for item in db_model.__table__.columns:
            if item.name not in base_user_log_model_columns and item.name not in base_model_columns:
                if isinstance(item, db.Model):
                    continue
                if item.name.startswith('_'):
                    continue
                if not item.default:
                    model_columns.update({item.name: None})
                elif hasattr(item.default.arg, '__call__'):  # noqa: B004
                    model_columns.update({item.name: item.default.arg(ctx=None)})
                else:
                    model_columns.update({item.name: item.default.arg})
    return model_columns
