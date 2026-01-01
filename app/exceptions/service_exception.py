class ExistanceError(Exception):
    """Exception raised when a requested resource does not exist."""
    pass
class UniquenessError(Exception):
    """Exception raised when a uniqueness constraint is violated."""
    pass