import os
from hashlib import pbkdf2_hmac
from typing import (
    Iterable,
    LiteralString,
)


class PasswordUtility:
    hashing_algorithm: LiteralString = f'sha256'

    def validate_password(
            self,
            password: str,
            password_hash: bytes,
            password_salt: bytes,
    ) -> bool:
        return password_hash == pbkdf2_hmac(
            hash_name=self.hashing_algorithm,
            password=password.encode(),
            salt=password_salt,
            iterations=100000,
            dklen=128,
        )

    def generate_hash(self, password: str) -> Iterable[bytes]:
        salt = self.generate_salt()
        hashed_password = self.hash_password(password, salt)
        return hashed_password, salt

    @staticmethod
    def generate_salt() -> bytes:
        return os.urandom(32)

    def hash_password(self, password: str, salt: bytes) -> bytes:
        return pbkdf2_hmac(
            hash_name=self.hashing_algorithm,
            password=password.encode(),
            salt=salt,
            iterations=100000,
            dklen=128,
        )
