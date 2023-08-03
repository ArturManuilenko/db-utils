import uuid
from typing import List

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin

from db_utils import CustomQuery
from db_utils.modules.db import db
from db_utils.utils.ensure.ensure_list import ensure_list
from db_utils.utils.remove_duplicated_spaces_of_string import remove_duplicated_spaces_of_string


class BaseMaterializedPGView(db.Model, SerializerMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    last_refresh_date = db.Column(db.DateTime(), nullable=False)

    sql = ''

    _index_format = '{table}_{field}_index'
    _pkey_format = '{table}_pkey'

    __abstract__ = True

    @classmethod
    def create_view(cls) -> None:
        assert isinstance(cls.sql, str)
        sql_string = cls.sql.strip()

        sql_create = f'CREATE MATERIALIZED VIEW {cls.__tablename__} AS ' + sql_string
        sql_index = ('' if sql_create[-1] == ';' else ';') + f'CREATE UNIQUE INDEX {cls._pkey_format.format(table=cls.__tablename__)} ON {cls.__tablename__}(id);'

        command = remove_duplicated_spaces_of_string(sql_create + sql_index)
        db.engine.execute(text(command))

        cls.query.filter().first()

    @classmethod
    def create_index(cls, field_names: List[str]) -> None:
        ensure_list(field_names, str)
        commands = list()
        for field_name in set(field_names):
            commands.append(f'CREATE INDEX {cls._index_format.format(table=cls.__tablename__, field=field_name)} ON {cls.__tablename__} ({field_name});')
        db.engine.execute(text(''.join(commands)))

    @classmethod
    def drop_index(cls, field_names: List[str]) -> None:
        ensure_list(field_names, str)
        commands = list()
        for field_name in set(field_names):
            commands.append(f'DROP INDEX {cls._index_format.format(table=cls.__tablename__, field=field_name)};')
        db.engine.execute(text(''.join(commands)))

    @classmethod
    def refresh_view(cls) -> None:
        db.engine.execute(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {cls.__tablename__};")

    @classmethod
    def drop_view(cls) -> None:
        db.engine.execute(f"DROP MATERIALIZED VIEW {cls.__tablename__};")
