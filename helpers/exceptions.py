class ApiServiceError(Exception):
    """Something went wrong with API"""

class KeyCreationError(ApiServiceError):
    """API error: cannot create key"""

class KeyRenamingError(ApiServiceError):
    """API error: cannot rename created key"""

class InvalidServerIdError(Exception):
    """Server ID does not exist"""

class InvalidGenaProfileLink(Exception):
    """The passed link is not a link to a gena profile."""
