from typing import Union
from uuid import UUID

from db_utils.model.base_model import BaseModel
from db_utils.modules.custom_query import CustomQuery
from db_utils.model.base_user_log_model import BaseUserLogModel
from sqlalchemy.orm.exc import NoResultFound as NoResultFoundError


def query_soft_delete(
    model: Union[BaseModel, BaseUserLogModel],
    instance_id: UUID,
    user_modified_id: UUID = None,
    query: CustomQuery = None
) -> Union[BaseModel, BaseUserLogModel]:
    if not issubclass(model, BaseUserLogModel) and not issubclass(model, BaseModel):
        raise ValueError(f'model must be inherited of {BaseModel} or {BaseUserLogModel}')
    if issubclass(model, BaseUserLogModel):
        assert user_modified_id is not None, "user_modified_id must be given"
    if query is not None:
        if not isinstance(query, CustomQuery):
            raise ValueError(f"query must be type of {CustomQuery}, got {type(query)}")
        instance = query\
            .with_deleted()\
            .filter(model.id == instance_id)\
            .first()
        if instance is None:
            raise NoResultFoundError(f'{model.__name__} not found')
        if instance.is_alive:
            if issubclass(model, BaseUserLogModel):
                instance.mark_as_deleted(user_modified_id)
            elif issubclass(model, BaseModel):
                instance.mark_as_deleted()
    else:
        instance = model.query\
            .with_deleted()\
            .filter(model.id == instance_id)\
            .first()
        if instance is None:
            raise NoResultFoundError(f'{model.__name__} not found')
        if instance.is_alive:
            if issubclass(model, BaseUserLogModel):
                instance.mark_as_deleted(user_modified_id)
            elif issubclass(model, BaseModel):
                instance.mark_as_deleted()
    return instance
