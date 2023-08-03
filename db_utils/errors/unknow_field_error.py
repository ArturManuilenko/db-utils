class UnknownFieldError(Exception):
    """Raised when the user attempts to reference a field that does not
    exist on a model in a search.

    """

    def __init__(self, field: str) -> None:

        #: The name of the unknown attribute.
        self.field = field
