from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.settings import settings


class AuthHelper:
    AUTH_SECRET_KEY = settings.AUTH_SECRET_KEY
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def create_token(self, useremail: str, expires_delta):
        data = {'sub': useremail}
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode, self.AUTH_SECRET_KEY, algorithm=self.ALGORITHM,
        )
        return encoded_jwt

    def create_access_token(self, useremail: str):
        expires_delta = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self.create_token(useremail, expires_delta=expires_delta)

    def create_refresh_token(self, useremail: str):
        expires = timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)
        return self.create_token(useremail, expires_delta=expires)

    def decode_token(self, token) -> str:
        payload = jwt.decode(
            token, self.AUTH_SECRET_KEY, algorithms=[self.ALGORITHM],
        )
        return payload.get('sub')


auth_helper = AuthHelper()
