from sqlalchemy import Column, String, UUID
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


Base.metadata.create_all(bind=DB_ENGINE)
