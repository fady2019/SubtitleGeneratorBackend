from sqlalchemy import Column, String, UUID
import uuid

from . import db_config as db


class User(db.Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def to_dict(self, include_email=False, include_password=False):
        user_obj = {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
        }

        if include_email:
            user_obj["email"] = self.email

        if include_password:
            user_obj["password"] = self.password

        return user_obj


db.Base.metadata.create_all(bind=db.DB_ENGINE)
