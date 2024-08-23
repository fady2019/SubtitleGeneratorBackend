from sqlalchemy import Column, Integer, Float, Text, UUID, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from db.db_config import Base, DB_ENGINE
from db.utils.entity_to_dict import generate_dict_from_entity


class SegmentEntity(Base):
    __tablename__ = "segments"
    segment_id = Column(Integer, nullable=False, info={"updatable": False})
    start = Column(Float, nullable=False, info={"updatable": False})
    end = Column(Float, nullable=False, info={"updatable": False})
    text = Column(Text, nullable=False)
    subtitle_id = Column(UUID(as_uuid=True), ForeignKey("subtitles.id"), nullable=False, info={"updatable": False})

    subtitle = relationship("SubtitleEntity", back_populates="segments")

    __table_args__ = (PrimaryKeyConstraint("segment_id", "subtitle_id"),)


Base.metadata.create_all(bind=DB_ENGINE)

generate_dict_from_entity(entity=SegmentEntity, ignore_if_exist=True)
