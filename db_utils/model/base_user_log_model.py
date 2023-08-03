from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from sqlalchemy.engine.base import Connection

import db_utils.modules.transaction_commit as transaction_commit
from db_utils.model.base_model import BaseModel
from db_utils.modules.db import db


class BaseUserLogModel(BaseModel):

    __abstract__ = True

    user_created_id = db.Column(pg_UUID(as_uuid=True), nullable=False)
    user_modified_id = db.Column(pg_UUID(as_uuid=True), nullable=False)

    def mark_as_created(  # type: ignore
            self,
            user_created_id: UUID,
            date_created: Optional[datetime] = None
    ) -> None:
        """Util for set user_created_id and date_created"""
        assert transaction_commit.transaction_context,\
            f'database insert must be in {transaction_commit} context manager'
        assert 'user_created_id' in [column.name for column in self.__table__.columns], \
            f"model {self.__repr__()} must have user_created_id foreign key"
        assert isinstance(user_created_id, UUID), f"user_created_id must be type of {UUID}"
        self.user_created_id = user_created_id
        self.user_modified_id = user_created_id
        if date_created:
            assert isinstance(date_created, datetime), f"date_created must be type of {datetime}"
            self.date_created = date_created
            self.date_modified = date_created
        else:
            self.date_created = datetime.utcnow()
            self.date_modified = datetime.utcnow()

    def mark_as_modified(  # type: ignore
            self,
            user_modified_id: UUID,
            date_modified: Optional[datetime] = None
    ) -> None:
        """Util for set user_modified_id and date_modified"""
        assert transaction_commit.transaction_context,\
            f'database update must be in {transaction_commit} context manager'
        assert isinstance(user_modified_id, UUID), f"user_modified_id must be type of {UUID}"
        self.user_modified_id = user_modified_id
        if date_modified is not None:
            assert isinstance(date_modified, datetime), f"date_modified must be type of {datetime}"
            self.date_modified = date_modified
        else:
            self.date_modified = datetime.utcnow()

    def mark_as_deleted(  # type: ignore
            self,
            user_modified_id: UUID,
            date_modified: Optional[datetime] = None
    ) -> None:
        """Util for set user_modified_id and date_modified"""
        assert transaction_commit.transaction_context,\
            f'database delete must be in {transaction_commit} context manager'

        assert isinstance(user_modified_id, UUID), \
            f"user_modified_id must be type of {UUID}, but {type(user_modified_id)} is given"

        self.user_modified_id = user_modified_id
        if date_modified is not None:
            assert isinstance(date_modified, datetime), \
                f"date_modified must be type of {datetime}, but {type(date_modified)} is given"

            self.date_modified = date_modified
        else:
            self.date_modified = datetime.utcnow()
        self.is_alive = False


@db.event.listens_for(db.Mapper, 'before_update')
def receive_before_update(mapper: db.Mapper, connection: Connection, target: BaseUserLogModel) -> None:
    if issubclass(target.__class__, BaseUserLogModel):
        assert transaction_commit.transaction_context,\
            f'database updates must be in {transaction_commit} context manager'

        unchanged_keys = inspect(target).attrs.get('id').state.unmodified

        assert 'date_modified' not in unchanged_keys, \
            "date_modified must be set on model update"

        assert isinstance(target.date_modified, datetime), \
            f"date_modified must be type of {datetime}, but {type(target.date_modified)} is given"

        assert 'user_modified_id' not in unchanged_keys,\
            "user_modified_id must be set on model update"

        assert isinstance(target.user_modified_id, UUID), \
            f"user_modified_id must be type of {UUID}, but {type(target.user_modified_id)} is given"


@db.event.listens_for(db.Mapper, 'before_insert')
def receive_before_create(mapper: db.Mapper, connection: Connection, target: BaseUserLogModel) -> None:
    if issubclass(target.__class__, BaseUserLogModel):
        assert transaction_commit.transaction_context,\
            f'database insert must be in {transaction_commit} context manager'
        assert isinstance(target.date_created, datetime), \
            f"date_created must be type of {datetime}, but {type(target.date_created)} is given"

        assert isinstance(target.date_modified, datetime), \
            f"date_modified must be type of {datetime}, but {type(target.date_modified)} is given"

        assert isinstance(target.user_created_id, UUID), \
            f"user_created_id must be type of {UUID}, but {type(target.user_created_id)} is given"

        assert isinstance(target.user_modified_id, UUID), \
            f"user_modified_id must be type of {UUID}, but {type(target.user_modified_id)} is given"
