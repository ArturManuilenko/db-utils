
class ComparisonToNullError(Exception):
    """Raised when a client attempts to use a filter object that compares a
    resource's attribute to ``NULL`` using the ``==`` operator instead of using
    ``is_null``.
    """
    pass
