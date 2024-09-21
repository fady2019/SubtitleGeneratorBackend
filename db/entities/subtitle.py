from sqlalchemy import Column, UUID, Enum, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid, enum, datetime

from db.db_config import Base, DB_ENGINE
from db.utils.entity_to_dict import generate_dict_from_entity


class SubtitleStatus(enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class SubtitleEntity(Base):
    __tablename__ = "subtitles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, info={"updatable": False, "excluded": True})
    title = Column(String(25), nullable=False, info={"updatable": True})
    status = Column(Enum(SubtitleStatus), nullable=False, default=SubtitleStatus.SCHEDULED, info={"excluded": True})
    language = Column(String(25), nullable=True, info={"excluded": True})
    translate = Column(Boolean, nullable=False, default=False, info={"updatable": False})
    start_date = Column(DateTime, nullable=True, info={"excluded": True})
    finish_date = Column(DateTime, nullable=True, info={"excluded": True})
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now, info={"updatable": False, "excluded": True})
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, info={"updatable": False})
    task_id = Column(UUID(as_uuid=True), nullable=True, info={"excluded": True})

    segments = relationship("SegmentEntity", back_populates="subtitle", cascade="all, delete-orphan")
    user = relationship("UserEntity", back_populates="subtitles")


Base.metadata.create_all(bind=DB_ENGINE)

generate_dict_from_entity(entity=SubtitleEntity, ignore_if_exist=False)
