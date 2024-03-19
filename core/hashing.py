import bcrypt


class Hasher:
    @staticmethod
    def hash_password(plain_password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode(encoding="utf-8"), salt)
        return hashed_password.decode(encoding="utf-8")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return bcrypt.checkpw(
            plain_password.encode(encoding="utf-8"),
            hashed_password.encode(encoding="utf-8"),
        )
