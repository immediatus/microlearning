"""
Creator database model.
"""
import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.guid import GUID


class Creator(Base):
    """Creator model for content creators."""

    __tablename__ = "creators"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    full_name = Column(String(100), nullable=True)
    bio = Column(String(500), nullable=True)
    avatar_url = Column(String(500), nullable=True)

    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    content_projects = relationship(
        "ContentProject", back_populates="creator", cascade="all, delete-orphan"
    )
    analytics_events = relationship("AnalyticsEvent", back_populates="creator")
    ai_service_costs = relationship(
        "AIServiceCost", back_populates="creator", cascade="all, delete-orphan"
    )
    budget = relationship(
        "CreatorBudget",
        back_populates="creator",
        uselist=False,
        cascade="all, delete-orphan",
    )
    approval_requests = relationship(
        "ApprovalRequest", back_populates="creator", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Creator(id={self.id}, username='{self.username}')>"
