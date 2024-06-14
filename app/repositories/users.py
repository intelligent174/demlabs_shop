from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.repository.base import BaseAlchemyRepository
from app.models.users import User
from app.schemas.fields.phone_number import PhoneNumber
from app.schemas.responses.users import UserCreateResponse

__all__ = [
    'UserRepository',
]


class UserRepository(BaseAlchemyRepository):
    model = User
    creation_schema = UserCreateResponse

    async def get_user_by_phone(
            self,
            phone: PhoneNumber,
            is_serialize: bool = True,
    ) -> User:
        stmt = (
            select(self.model)
            .where(self.model.phone == phone)
        )

        async with self._db.get_session() as session:
            try:
                db_result = await session.execute(stmt)
                user = db_result.scalar_one()
            except SQLAlchemyError as e:
                raise e

            return self.serialize(user) if is_serialize else user
