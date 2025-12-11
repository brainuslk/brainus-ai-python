"""Custom exceptions for the Brainus AI SDK."""


class BrainusError(Exception):
    """Base exception for all Brainus AI errors."""

    pass


class AuthenticationError(BrainusError):
    """Raised when API key is invalid or missing."""

    pass


class RateLimitError(BrainusError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int | None = None):
        super().__init__(message)
        self.retry_after = retry_after


class QuotaExceededError(BrainusError):
    """Raised when monthly quota is exceeded."""

    pass


class APIError(BrainusError):
    """Raised for general API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code



