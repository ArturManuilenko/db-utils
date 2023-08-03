# type: ignore
# noqa
"""
    Helper functions from Flask-Restless
    for db_search util
"""
import datetime

from db_utils.errors.unknow_field_error import UnknownFieldError
from dateutil.parser import parse as parse_datetime
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Interval
from sqlalchemy import Time
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import RelationshipProperty as RelProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.inspection import inspect as sqlalchemy_inspect


#: Names of attributes which should definitely not be considered relations when
#: dynamically computing a list of relations of a SQLAlchemy model.
RELATION_BLACKLIST = ('query', 'query_class', '_sa_class_manager',
                      '_decl_class_registry')

#: Types which should be considered columns of a model when iterating over all
#: attributes of a model class.
COLUMN_TYPES = (InstrumentedAttribute, hybrid_property)

#: Strings which, when received by the server as the value of a date or time
#: field, indicate that the server should use the current time when setting the
#: value of the field.
CURRENT_TIME_MARKERS = ('CURRENT_TIMESTAMP', 'CURRENT_DATE', 'LOCALTIMESTAMP')


def session_query(model):
    """Returns a SQLAlchemy query object for the specified `model`.

    If `model` has a ``query`` attribute already, ``model.query`` will be
    returned. If the ``query`` attribute is callable ``model.query()`` will be
    returned instead.

    """
    if hasattr(model, 'query'):
        if callable(model.query):
            query = model.query()
        else:
            query = model.query
        if hasattr(query, 'filter'):
            return query


def get_relations(model):
    """Returns a list of tuples (relation name, relations propertis) of `model`."""
    relations = sqlalchemy_inspect(model).relationships.items()
    return [relation for relation in relations if relation[0] not in RELATION_BLACKLIST]


def get_related_model(model, relationname):
    """Gets the class of the model to which `model` is related by the attribute
    whose name is `relationname`.

    For example, if we have the model classes ::

        class Person(Base):
            __tablename__ = 'person'
            id = Column(Integer, primary_key=True)
            articles = relationship('Article')

        class Article(Base):
            __tablename__ = 'article'
            id = Column(Integer, primary_key=True)
            author_id = Column(Integer, ForeignKey('person.id'))
            author = relationship('Person')

    then

        >>> get_related_model(Person, 'articles')
        <class 'Article'>
        >>> get_related_model(Article, 'author')
        <class 'Person'>

    """
    if hasattr(model, relationname):
        # inspector = sqlalchemy_inspect(model)
        # attributes = inspector.attrs
        # if relationname in attributes:
        #     state = attributes[relationname]
        attr = getattr(model, relationname)
        if hasattr(attr, 'property') \
                and isinstance(attr.property, RelProperty):
            return attr.property.mapper.class_
        if isinstance(attr, AssociationProxy):
            return get_related_association_proxy_model(attr)
    raise UnknownFieldError(
        f"{model.__name__} have not attached object '{relationname}'"
    )


def get_related_association_proxy_model(attr):
    """Returns the model class specified by the given SQLAlchemy relation
    attribute, or ``None`` if no such class can be inferred.

    `attr` must be a relation attribute corresponding to an association proxy.

    """
    prop = attr.remote_attr.property
    for attribute in ('mapper', 'parent'):
        if hasattr(prop, attribute):
            return getattr(prop, attribute).class_
    return None


def get_field_type(model, fieldname):
    """Helper which returns the SQLAlchemy type of the field."""
    field = getattr(model, fieldname)
    if isinstance(field, ColumnElement):
        return field.type
    if isinstance(field, AssociationProxy):
        field = field.remote_attr
    if hasattr(field, 'property'):
        prop = field.property
        if isinstance(prop, RelProperty):
            return None
        return prop.columns[0].type
    return None


def is_like_list(instance, relation):
    """Returns ``True`` if and only if the relation of `instance` whose name is
    `relation` is list-like.

    A relation may be like a list if, for example, it is a non-lazy one-to-many
    relation, or it is a dynamically loaded one-to-many.

    """
    if relation in instance._sa_class_manager:
        if hasattr(instance._sa_class_manager[relation].property, 'uselist'):
            return instance._sa_class_manager[relation].property.uselist
        else:
            return False
    elif hasattr(instance, relation):
        attr = getattr(instance._sa_instance_state.class_, relation)
        if hasattr(attr, 'property'):
            return attr.property.uselist
    related_value = getattr(type(instance), relation, None)
    if isinstance(related_value, AssociationProxy):
        local_prop = related_value.local_attr.prop
        if isinstance(local_prop, RelProperty):
            return local_prop.uselist
    return False


def string_to_datetime(model, fieldname, value):
    """Casts `value` to a :class:`datetime.datetime` or
    :class:`datetime.timedelta` object if the given field of the given
    model is a date-like or interval column.

    If the field name corresponds to a field in the model which is a
    :class:`sqlalchemy.types.Date`, :class:`sqlalchemy.types.DateTime`,
    or :class:`sqlalchemy.Interval`, then the returned value will be the
    :class:`datetime.datetime` or :class:`datetime.timedelta` Python
    object corresponding to `value`. Otherwise, the `value` is returned
    unchanged.

    """
    if value is None:
        return value
    # If this is a date, time or datetime field, parse it and convert it to
    # the appropriate type.
    field_type = get_field_type(model, fieldname)
    if isinstance(field_type, (Date, Time, DateTime)):
        # If the string is empty, no datetime can be inferred from it.
        if value.strip() == '':
            return None
        # If the string is a string indicating that the value of should be the
        # current datetime on the server, get the current datetime that way.
        if value in CURRENT_TIME_MARKERS:
            return getattr(func, value.lower())()
        value_as_datetime = parse_datetime(value)
        # If the attribute on the model needs to be a Date or Time object as
        # opposed to a DateTime object, just get the date component of the
        # datetime.
        if isinstance(field_type, Date):
            return value_as_datetime.date()
        if isinstance(field_type, Time):
            return value_as_datetime.timetz()
        return value_as_datetime
    # If this is an Interval field, convert the integer value to a timedelta.
    if isinstance(field_type, Interval) and isinstance(value, int):
        return datetime.timedelta(seconds=value)
    # In any other case, simply copy the value unchanged.
    return value


def strings_to_datetimes(model, dictionary):
    """Returns a new dictionary with all the mappings of `dictionary` but
    with date strings and intervals mapped to :class:`datetime.datetime` or
    :class:`datetime.timedelta` objects.

    The keys of `dictionary` are names of fields in the model specified in the
    constructor of this class. The values are values to set on these fields. If
    a field name corresponds to a field in the model which is a
    :class:`sqlalchemy.types.Date`, :class:`sqlalchemy.types.DateTime`, or
    :class:`sqlalchemy.Interval`, then the returned dictionary will have the
    corresponding :class:`datetime.datetime` or :class:`datetime.timedelta`
    Python object as the value of that mapping in place of the string.

    This function outputs a new dictionary; it does not modify the argument.

    """
    # In Python 2.7+, this should be a dict comprehension.
    return dict((k, string_to_datetime(model, k, v))
                for k, v in dictionary.items() if k not in ('type', 'links'))


def enshure_attribute(instance, attribute_name):
    try:
        field = getattr(instance, attribute_name)
    except AttributeError:
        raise UnknownFieldError(
            f"{instance.__name__} have not attribute '{attribute_name}'"
        )
    return field
