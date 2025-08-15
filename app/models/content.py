"""
Content database models for videos and learning materials
"""

from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean, Text, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from enum import Enum
import uuid

from app.core.database import Base


class ContentStatus(str, Enum):
    """Content status enumeration."""
    DRAFT = "draft"
    GENERATING = "generating" 
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class LearningVideo(Base):
    """Learning video content model."""
    
    __tablename__ = "learning_videos"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=False, index=True)
    concept = Column(String(500), nullable=False)  # original concept prompt
    
    # Content
    script_content = Column(Text, nullable=False)
    learning_objectives = Column(ARRAY(String), nullable=False)
    
    # Video assets
    video_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    preview_url = Column(String(500), nullable=True)  # low-quality preview
    
    # Video properties
    duration_seconds = Column(Integer, nullable=False)
    resolution = Column(String(20), default="1080x1920")  # 9:16 aspect ratio
    file_size_bytes = Column(Integer, nullable=True)
    encoding_format = Column(String(10), default="mp4")
    
    # Educational metadata
    difficulty_level = Column(Integer, nullable=False)  # 1-10 scale
    age_groups = Column(ARRAY(String), nullable=False)  # ["12-15"]
    subject_area = Column(String(100), nullable=False)  # "Physics", "Chemistry", etc.
    curriculum_standards = Column(ARRAY(String), default=list)  # aligned standards
    
    # Quiz data
    quiz_questions = Column(JSON, nullable=False)  # embedded quiz questions
    quiz_count = Column(Integer, default=0)
    
    # Engagement metrics
    view_count = Column(Integer, default=0)
    completion_rate = Column(Float, default=0.0)  # percentage
    average_quiz_score = Column(Float, default=0.0)  # percentage
    like_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    bookmark_count = Column(Integer, default=0)
    
    # Performance metrics
    popularity_score = Column(Float, default=0.0)  # calculated score
    engagement_score = Column(Float, default=0.0)  # time watched / duration
    educational_effectiveness = Column(Float, default=0.0)  # learning outcome score
    
    # Content status
    status = Column(String(20), default=ContentStatus.DRAFT, index=True)
    is_featured = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    
    # AI generation metadata
    generation_config = Column(JSON, default=dict)  # AI generation parameters
    ai_confidence_score = Column(Float, nullable=True)  # AI confidence in content
    human_review_notes = Column(Text, nullable=True)
    
    # Quality assurance
    qa_results = Column(JSON, default=dict)  # QA check results
    factual_accuracy_score = Column(Float, nullable=True)
    age_appropriateness_score = Column(Float, nullable=True)
    engagement_prediction = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)
    last_viewed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<LearningVideo(id={self.id}, title={self.title}, topic={self.topic})>"
    
    @property
    def is_published(self) -> bool:
        """Check if video is published and available."""
        return self.status == ContentStatus.PUBLISHED
    
    @property
    def age_group_primary(self) -> str:
        """Get primary age group."""
        return self.age_groups[0] if self.age_groups else "12-15"
    
    @property
    def duration_minutes(self) -> float:
        """Get duration in minutes."""
        return self.duration_seconds / 60.0


class ContentProject(Base):
    """Content creation project model for tracking AI generation."""
    
    __tablename__ = "content_projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Input parameters
    concept_prompt = Column(Text, nullable=False)
    age_group = Column(String(20), nullable=False)
    difficulty_level = Column(Integer, default=5)
    subject_area = Column(String(100), nullable=False)
    
    # Generation status
    status = Column(String(50), default="initializing", index=True)
    current_step = Column(String(100), nullable=True)
    progress_percentage = Column(Integer, default=0)
    
    # Generated content
    ai_generated_script = Column(Text, nullable=True)
    visual_storyboard = Column(JSON, default=dict)
    voice_config = Column(JSON, default=dict)
    music_config = Column(JSON, default=dict)
    
    # Human edits
    human_edited_script = Column(Text, nullable=True)
    visual_modifications = Column(JSON, default=dict)
    approval_notes = Column(Text, nullable=True)
    
    # Quality assurance
    qa_results = Column(JSON, default=dict)
    qa_passed = Column(Boolean, default=False)
    manual_review_required = Column(Boolean, default=False)
    
    # Processing metadata
    generation_start_time = Column(DateTime(timezone=True), nullable=True)
    generation_end_time = Column(DateTime(timezone=True), nullable=True)
    total_generation_time = Column(Integer, nullable=True)  # seconds
    
    # Cost tracking
    ai_service_costs = Column(JSON, default=dict)  # cost breakdown by service
    total_cost_usd = Column(Float, default=0.0)
    
    # Error handling
    errors = Column(JSON, default=list)
    retry_count = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)
    
    # Output
    published_video_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<ContentProject(id={self.id}, status={self.status}, concept={self.concept_prompt[:50]})>"
    
    @property
    def is_completed(self) -> bool:
        """Check if project is completed."""
        return self.status in ["approved", "published"]
    
    @property
    def generation_duration_minutes(self) -> float:
        """Get generation duration in minutes."""
        if self.total_generation_time:
            return self.total_generation_time / 60.0
        return 0.0


class ContentTemplate(Base):
    """Visual and structural templates for content generation."""
    
    __tablename__ = "content_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)  # subject area
    
    # Template configuration
    template_config = Column(JSON, nullable=False)
    visual_style = Column(JSON, default=dict)
    animation_presets = Column(JSON, default=dict)
    color_scheme = Column(JSON, default=dict)
    
    # Usage metadata
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)  # percentage of successful generations
    average_rating = Column(Float, default=0.0)
    
    # Template properties
    age_groups = Column(ARRAY(String), nullable=False)
    difficulty_levels = Column(ARRAY(Integer), default=list)  # supported difficulty levels
    estimated_duration = Column(Integer, default=60)  # seconds
    
    # Template assets
    preview_url = Column(String(500), nullable=True)
    asset_urls = Column(JSON, default=dict)  # URLs to template assets
    
    # Status
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<ContentTemplate(id={self.id}, name={self.name}, category={self.category})>"


class ContentTag(Base):
    """Tags for categorizing and organizing content."""
    
    __tablename__ = "content_tags"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False)  # topic, difficulty, format, etc.
    description = Column(Text, nullable=True)
    
    # Usage statistics
    usage_count = Column(Integer, default=0)
    content_count = Column(Integer, default=0)  # number of videos with this tag
    
    # Display properties
    color = Column(String(7), nullable=True)  # hex color code
    icon = Column(String(50), nullable=True)  # icon identifier
    display_order = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<ContentTag(id={self.id}, name={self.name}, category={self.category})>"