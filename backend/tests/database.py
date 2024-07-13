from passlib.context import CryptContext

password = "123456"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context.hash(password)


