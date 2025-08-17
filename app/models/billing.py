"""
Billing and cost-tracking database models.
"""

from decimal import Decimal
from datetime import datetime
from enum import Enum
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.guid import GUID


class AIServiceType(str, Enum):
    """AI service types for cost tracking."""
    OPENAI_GPT = "openai_gpt"
    OPENAI_DALLE = "openai_dalle"
    ANTHROPIC_CLAUDE = "anthropic_claude"
    ELEVENLABS_TTS = "elevenlabs_tts"
    AZURE_SPEECH = "azure_speech"
    GOOGLE_TTS = "google_tts"
    RUNWAY_VIDEO = "runway_video"
    PIKA_VIDEO = "pika_video"
    STABLE_DIFFUSION = "stable_diffusion"
    MIDJOURNEY = "midjourney"
    SUNO_MUSIC = "suno_music"
    AIVA_MUSIC = "aiva_music"
    DID_AVATAR = "did_avatar"
    SYNTHESIA_AVATAR = "synthesia_avatar"


class ApprovalStatus(str, Enum):
    """Approval status for AI operations."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTO_APPROVED = "auto_approved"
    EXPIRED = "expired"


class CostTier(str, Enum):
    """Cost tiers for approval thresholds."""
    LOW = "low"          # < $1
    MEDIUM = "medium"    # $1 - $10
    HIGH = "high"        # $10 - $100
    CRITICAL = "critical" # > $100


class AIServiceCost(Base):
    """Database model for tracking AI service costs."""

    __tablename__ = "ai_service_costs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)

    # Service identification
    service_type = Column(String(100), nullable=False, index=True)
    service_model = Column(String(100), nullable=True)
    operation_type = Column(String(100), nullable=False)  # generation, synthesis, etc.

    # Cost information
    estimated_cost = Column(Numeric(10, 4), nullable=False)  # Estimated cost in USD
    actual_cost = Column(Numeric(10, 4), nullable=True)     # Actual cost from provider
    cost_tier = Column(String(20), nullable=False, index=True)
    currency = Column(String(3), default="USD")

    # Usage metrics
    tokens_used = Column(Integer, nullable=True)
    characters_processed = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    image_count = Column(Integer, nullable=True)
    video_duration = Column(Integer, nullable=True)

    # Request details
    request_parameters = Column(JSON, nullable=False)
    response_metadata = Column(JSON, nullable=True)

    # Project context
    project_id = Column(GUID, ForeignKey("content_projects.id"), nullable=True, index=True)
    creator_id = Column(GUID, ForeignKey("creators.id"), nullable=False, index=True)
    content_type = Column(String(50), nullable=False)  # script, image, voice, etc.

    # Relationships
    creator = relationship("Creator", back_populates="ai_service_costs")
    project = relationship("ContentProject", back_populates="cost_entries")
    approval_request = relationship("ApprovalRequest", back_populates="cost_entry", uselist=False)

    # Approval workflow
    approval_status = Column(String(20), default=ApprovalStatus.PENDING, index=True)
    requires_approval = Column(Boolean, default=True)
    approved_by = Column(GUID, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    # Processing status
    is_processed = Column(Boolean, default=False)
    processing_started_at = Column(DateTime, nullable=True)
    processing_completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    # Cache info
    cache_hit = Column(Boolean, default=False)
    cache_key = Column(String(255), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<AIServiceCost(id={self.id}, service={self.service_type}, cost=${self.estimated_cost})>"


class CreatorBudget(Base):
    """Database model for creator budget management."""

    __tablename__ = "creator_budgets"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    creator_id = Column(GUID, ForeignKey("creators.id"), nullable=False, unique=True, index=True)

    # Relationships
    creator = relationship("Creator", back_populates="budget")

    # Budget limits
    daily_limit = Column(Numeric(10, 2), default=Decimal("50.00"))
    weekly_limit = Column(Numeric(10, 2), default=Decimal("200.00"))
    monthly_limit = Column(Numeric(10, 2), default=Decimal("500.00"))

    # Current usage
    daily_spent = Column(Numeric(10, 2), default=Decimal("0.00"))
    weekly_spent = Column(Numeric(10, 2), default=Decimal("0.00"))
    monthly_spent = Column(Numeric(10, 2), default=Decimal("0.00"))

    # Auto-approval thresholds
    auto_approve_threshold = Column(Numeric(10, 2), default=Decimal("5.00"))
    require_approval_above = Column(Numeric(10, 2), default=Decimal("25.00"))

    # Budget period tracking
    daily_reset_at = Column(DateTime, nullable=False)
    weekly_reset_at = Column(DateTime, nullable=False)
    monthly_reset_at = Column(DateTime, nullable=False)

    # Status
    is_active = Column(Boolean, default=True)
    is_suspended = Column(Boolean, default=False)
    suspension_reason = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<CreatorBudget(creator_id={self.creator_id}, daily_limit=${self.daily_limit})>"


class ApprovalRequest(Base):
    """Database model for AI operation approval requests."""

    __tablename__ = "approval_requests"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    cost_entry_id = Column(GUID, ForeignKey("ai_service_costs.id"), nullable=False, index=True)
    creator_id = Column(GUID, ForeignKey("creators.id"), nullable=False, index=True)

    # Relationships
    cost_entry = relationship("AIServiceCost", back_populates="approval_request")
    creator = relationship("Creator", back_populates="approval_requests")

    # Request details
    operation_description = Column(Text, nullable=False)
    estimated_cost = Column(Numeric(10, 4), nullable=False)
    cost_tier = Column(String(20), nullable=False)

    # Approval details
    status = Column(String(20), default=ApprovalStatus.PENDING, index=True)
    approved_by = Column(GUID, nullable=True)
    approval_method = Column(String(50), nullable=True)  # manual, auto, budget_check

    # Timing
    expires_at = Column(DateTime, nullable=False)  # Auto-reject after expiration
    approved_at = Column(DateTime, nullable=True)

    # Notes
    approval_notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ApprovalRequest(id={self.id}, cost=${self.estimated_cost}, status={self.status})>"
