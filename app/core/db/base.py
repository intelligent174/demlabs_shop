from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

__all__ = [
    'Database',
]


class Database:
    def __init__(
            self,
            dsn_url: str,
            echo: bool = False,
    ) -> None:
        self._async_engine = create_async_engine(
            url=str(dsn_url),
            future=True,
            echo=echo,
        )
        self._async_session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        self._session_factory = async_scoped_session(
            session_factory=self._async_session_factory,
            scopefunc=current_task,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
