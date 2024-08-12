from sqlalchemy import Column, String, UUID, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from db.db_config import Base, DB_ENGINE
from db.utils.entity_to_dict import generate_dict_from_entity


class TemporaryTokenType(enum.Enum):
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"


class TemporaryTokenEntity(Base):
    __tablename__ = "temporary_tokens"
    token = Column(String, primary_key=True, info={"updatable": False})
    expiration_date = Column(DateTime, nullable=False, info={"updatable": False})
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, info={"updatable": False})
    type = Column(Enum(TemporaryTokenType), nullable=False, info={"updatable": False})

    user = relationship("UserEntity", back_populates="temp_tokens")


Base.metadata.create_all(bind=DB_ENGINE)

generate_dict_from_entity(TemporaryTokenEntity, ignore_if_exist=True)
