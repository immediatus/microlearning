"""
Student database models
"""

from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Student(Base):
    """Student model for user data and progress tracking."""
    
    __tablename__ = "students"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    age_group = Column(String(10), nullable=False, index=True)  # e.g., "12-15"
    
    # Learning preferences and settings
    learning_preferences = Column(JSON, default=dict)  # personalization data
    notification_settings = Column(JSON, default=dict)  # push notification preferences
    accessibility_settings = Column(JSON, default=dict)  # accessibility options
    
    # Progress tracking
    streak_count = Column(Integer, default=0)  # consecutive days of learning
    total_videos_watched = Column(Integer, default=0)
    total_quiz_correct = Column(Integer, default=0)
    total_quiz_attempts = Column(Integer, default=0)
    
    # Achievement data
    achievements_unlocked = Column(ARRAY(String), default=list)  # list of achievement IDs
    badges_earned = Column(ARRAY(String), default=list)  # list of badge IDs
    current_level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    
    # Learning path data
    completed_topics = Column(ARRAY(String), default=list)  # list of topic IDs
    current_learning_path = Column(String(255), nullable=True)  # current path ID
    preferred_difficulty = Column(Integer, default=5)  # 1-10 scale
    
    # Engagement metrics
    average_session_duration = Column(Integer, default=0)  # in seconds
    last_video_watched = Column(UUID(as_uuid=True), nullable=True)
    favorite_topics = Column(ARRAY(String), default=list)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    parent_email = Column(String(255), nullable=True)  # for under-13 users
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now())
    streak_updated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Student(id={self.id}, username={self.username}, age_group={self.age_group})>"
    
    @property
    def quiz_accuracy(self) -> float:
        """Calculate quiz accuracy percentage."""
        if self.total_quiz_attempts == 0:
            return 0.0
        return (self.total_quiz_correct / self.total_quiz_attempts) * 100
    
    @property
    def is_beginner(self) -> bool:
        """Check if student is a beginner (watched < 10 videos)."""
        return self.total_videos_watched < 10
    
    @property
    def engagement_level(self) -> str:
        """Determine engagement level based on activity."""
        if self.total_videos_watched == 0:
            return "new"
        elif self.total_videos_watched < 5:
            return "low"
        elif self.total_videos_watched < 20:
            return "medium"
        else:
            return "high"


class StudentSession(Base):
    """Model for tracking individual learning sessions."""
    
    __tablename__ = "student_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Session data
    session_start = Column(DateTime(timezone=True), server_default=func.now())
    session_end = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, default=0)
    
    # Content consumed
    videos_watched = Column(Integer, default=0)
    quizzes_completed = Column(Integer, default=0)
    quizzes_correct = Column(Integer, default=0)
    
    # Context
    device_type = Column(String(50), nullable=True)  # mobile, tablet, web
    app_version = Column(String(20), nullable=True)
    
    # Performance metrics
    average_video_completion = Column(Integer, default=0)  # percentage
    average_quiz_response_time = Column(Integer, default=0)  # milliseconds
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<StudentSession(id={self.id}, student_id={self.student_id}, duration={self.duration_seconds})>"


class StudentPreference(Base):
    """Model for storing detailed student preferences."""
    
    __tablename__ = "student_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Learning preferences
    preferred_video_duration = Column(Integer, default=60)  # seconds
    preferred_learning_time = Column(String(20), nullable=True)  # morning, afternoon, evening
    preferred_topics = Column(ARRAY(String), default=list)
    avoided_topics = Column(ARRAY(String), default=list)
    
    # Interface preferences
    dark_mode = Column(Boolean, default=False)
    auto_play_next = Column(Boolean, default=True)
    show_captions = Column(Boolean, default=False)
    haptic_feedback = Column(Boolean, default=True)
    
    # Notification preferences
    daily_reminder = Column(Boolean, default=True)
    streak_notifications = Column(Boolean, default=True)
    achievement_notifications = Column(Boolean, default=True)
    learning_tips = Column(Boolean, default=True)
    
    # Parental controls
    max_daily_screen_time = Column(Integer, nullable=True)  # minutes
    allowed_topics = Column(ARRAY(String), nullable=True)  # restricted topic list
    parent_notifications = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<StudentPreference(student_id={self.student_id})>"