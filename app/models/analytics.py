"""
Analytics database models.
"""
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.guid import GUID


class AnalyticsEvent(Base):
    """A flexible model for storing various analytics events."""

    __tablename__ = "analytics_events"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)

    # The type of event, e.g., "video_view", "quiz_response", "share_content"
    event_type = Column(String(100), nullable=False, index=True)

    # Foreign keys to link events to specific entities (optional)
    student_id = Column(GUID, ForeignKey("students.id"), nullable=True, index=True)
    creator_id = Column(GUID, ForeignKey("creators.id"), nullable=True, index=True)
    video_id = Column(GUID, ForeignKey("learning_videos.id"), nullable=True, index=True)
    quiz_id = Column(GUID, ForeignKey("quizzes.id"), nullable=True, index=True)

    # A JSON blob to store any additional data related to the event
    # e.g., {"duration_watched": 30, "completed": false} for a video_view event
    payload = Column(JSON, nullable=True)

    # Timestamp for when the event occurred
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships to easily access related objects
    student = relationship("Student")
    creator = relationship("Creator")
    video = relationship("LearningVideo")
    quiz = relationship("Quiz")

    def __repr__(self):
        return f"<AnalyticsEvent(id={self.id}, type='{self.event_type}', student_id={self.student_id})>"
