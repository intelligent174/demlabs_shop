from asyncpg import CheckViolationError, ForeignKeyViolationError, UniqueViolationError

CastViolationError = (
    UniqueViolationError,
    CheckViolationError,
    ForeignKeyViolationError,
)
