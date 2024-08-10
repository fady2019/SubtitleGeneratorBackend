from sqlalchemy import Column, String, UUID, Boolean
from sqlalchemy.orm import relationship
import uuid

from db.db_config import Base, DB_ENGINE


class UserEntity(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)

    temp_tokens = relationship("TemporaryTokenEntity", back_populates="user", cascade="all, delete-orphan")


Base.metadata.create_all(bind=DB_ENGINE)
