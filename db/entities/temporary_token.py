from sqlalchemy import Column, String, UUID, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from db.db_config import Base, DB_ENGINE


class TemporaryTokenType(enum.Enum):
    PASSWORD_RESET = "password_reset"


class TemporaryTokenEntity(Base):
    __tablename__ = "temporary_tokens"
    token = Column(String, primary_key=True)
    expiration_date = Column(DateTime, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(Enum(TemporaryTokenType), nullable=False)

    user = relationship("UserEntity", back_populates="temp_tokens")


Base.metadata.create_all(bind=DB_ENGINE)
