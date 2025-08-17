"""
Quiz database models.
"""
import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.guid import GUID


class Quiz(Base):
    """
    Quiz model associated with a learning video.
    Each instance represents a single question.
    """

    __tablename__ = "quizzes"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    video_id = Column(GUID, ForeignKey("learning_videos.id"), nullable=False, index=True)

    question = Column(String(1000), nullable=False)
    # Storing options as a JSON object, e.g., {"a": "Option A", "b": "Option B"}
    options = Column(JSON, nullable=False)
    # Storing the key of the correct option, e.g., "a"
    correct_answer = Column(String(10), nullable=False)
    explanation = Column(String(2000), nullable=True)

    # The position of the quiz within the video's sequence
    order = Column(Integer, default=0)

    # Relationship to LearningVideo (back-populates a 'quizzes' attribute)
    video = relationship("LearningVideo", back_populates="quizzes")
    responses = relationship("QuizResponse", back_populates="quiz", cascade="all, delete-orphan")
    analytics_events = relationship("AnalyticsEvent", back_populates="quiz")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Quiz(id={self.id}, video_id={self.video_id}, question='{self.question[:30]}...')>"


class QuizResponse(Base):
    """Model to store a student's response to a quiz question."""

    __tablename__ = "quiz_responses"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    student_id = Column(GUID, ForeignKey("students.id"), nullable=False, index=True)
    quiz_id = Column(GUID, ForeignKey("quizzes.id"), nullable=False, index=True)
    video_id = Column(GUID, ForeignKey("learning_videos.id"), nullable=False, index=True)

    # The answer submitted by the student, e.g., "b"
    submitted_answer = Column(String(10), nullable=False)
    is_correct = Column(Boolean, nullable=False)

    # Time taken to answer in milliseconds
    response_time_ms = Column(Integer, nullable=True)

    # Relationships
    student = relationship("Student", back_populates="quiz_responses")
    quiz = relationship("Quiz", back_populates="responses")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<QuizResponse(student_id={self.student_id}, quiz_id={self.quiz_id}, correct={self.is_correct})>"
