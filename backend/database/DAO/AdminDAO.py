from database.table import Admin, BaseService
from schemas.admin import User, UserInDB


class AdminDAO:
    @staticmethod
    def insert(username: str, password: str):
        new_user = Admin(username=username, password=password)
        BaseService.session.add(new_user)
        BaseService.session.commit()

    @staticmethod
    def get_user(username: str) -> UserInDB | None:
        user = (
            BaseService.session.query(Admin).filter(Admin.username == username).first()
        )
        if user is None:
            return None
        return UserInDB(username=user.username, hashed_password=user.password, disabled=user.disabled)
