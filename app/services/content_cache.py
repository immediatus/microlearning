"""
Content caching system to prevent regeneration and reduce AI service costs
"""

import hashlib
import json
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional

import aioredis
import structlog
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.config import settings
from app.core.database import Base, get_db

logger = structlog.get_logger()


class CacheType(str, Enum):
    """Cache type enumeration."""

    SCRIPT = "script"
    IMAGE = "image"
    VOICE = "voice"
    VIDEO = "video"
    MUSIC = "music"
    QUIZ = "quiz"
    COMPLETE_CONTENT = "complete_content"


class CacheStrategy(str, Enum):
    """Cache strategy enumeration."""

    EXACT_MATCH = "exact_match"  # Exact parameter match
    SEMANTIC_MATCH = "semantic_match"  # Similar concept match
    TEMPLATE_MATCH = "template_match"  # Template-based match
    FUZZY_MATCH = "fuzzy_match"  # Fuzzy parameter match


# Database model for persistent caching
class ContentCacheEntry(Base):
    """Database model for caching generated content."""

    __tablename__ = "content_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cache_key = Column(String(255), unique=True, nullable=False, index=True)
    content_hash = Column(String(64), nullable=False, index=True)  # SHA-256 hash

    # Cache metadata
    cache_type = Column(String(50), nullable=False, index=True)
    content_type = Column(
        String(100), nullable=False
    )  # script, image_url, audio_url, etc.

    # Input parameters (for matching)
    input_parameters = Column(JSON, nullable=False)
    normalized_params = Column(JSON, nullable=False)  # Normalized for fuzzy matching

    # Cached content
    content_data = Column(JSON, nullable=False)  # The actual generated content
    metadata = Column(JSON, default=dict)  # Additional metadata

    # Usage statistics
    hit_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, nullable=True)
    generation_cost = Column(String(20), nullable=True)  # Cost in USD
    generation_time = Column(Integer, nullable=True)  # Time in seconds

    # Cache management
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    quality_score = Column(Integer, default=5)  # 1-10 rating

    # AI service info
    ai_service = Column(String(100), nullable=True)
    ai_model = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ContentCacheEntry(id={self.id}, type={self.cache_type}, hits={self.hit_count})>"


class ContentCacheManager:
    """Manager for content caching with multiple strategies."""

    def __init__(self):
        self.redis_client: Optional[aioredis.Redis] = None
        self.cache_config = {
            CacheType.SCRIPT: {
                "ttl": 86400 * 30,  # 30 days
                "max_size": 1000,
                "strategy": CacheStrategy.SEMANTIC_MATCH,
            },
            CacheType.IMAGE: {
                "ttl": 86400 * 7,  # 7 days
                "max_size": 500,
                "strategy": CacheStrategy.FUZZY_MATCH,
            },
            CacheType.VOICE: {
                "ttl": 86400 * 14,  # 14 days
                "max_size": 200,
                "strategy": CacheStrategy.EXACT_MATCH,
            },
            CacheType.VIDEO: {
                "ttl": 86400 * 7,  # 7 days
                "max_size": 100,
                "strategy": CacheStrategy.TEMPLATE_MATCH,
            },
            CacheType.QUIZ: {
                "ttl": 86400 * 60,  # 60 days
                "max_size": 2000,
                "strategy": CacheStrategy.SEMANTIC_MATCH,
            },
            CacheType.COMPLETE_CONTENT: {
                "ttl": 86400 * 14,  # 14 days
                "max_size": 50,
                "strategy": CacheStrategy.EXACT_MATCH,
            },
        }

    async def initialize(self):
        """Initialize Redis connection."""
        try:
            self.redis_client = aioredis.from_url(
                settings.REDIS_URL, decode_responses=True, encoding="utf-8"
            )
            await self.redis_client.ping()
            logger.info("Content cache manager initialized")
        except Exception as e:
            logger.error(f"Failed to initialize cache manager: {e}")
            self.redis_client = None

    def _create_cache_key(
        self, cache_type: CacheType, parameters: dict[str, Any]
    ) -> str:
        """Create a unique cache key from parameters."""
        # Normalize parameters for consistent hashing
        normalized = self._normalize_parameters(parameters)
        param_string = json.dumps(normalized, sort_keys=True)

        # Create hash
        content_hash = hashlib.sha256(param_string.encode()).hexdigest()
        return f"content_cache:{cache_type}:{content_hash[:16]}"

    def _normalize_parameters(self, parameters: dict[str, Any]) -> dict[str, Any]:
        """Normalize parameters for consistent matching."""
        normalized = {}

        for key, value in parameters.items():
            if isinstance(value, str):
                # Normalize text: lowercase, strip whitespace, remove extra spaces
                normalized[key] = " ".join(value.lower().strip().split())
            elif isinstance(value, (int, float)):
                normalized[key] = value
            elif isinstance(value, list):
                # Sort lists for consistent ordering
                normalized[key] = (
                    sorted(value) if all(isinstance(x, str) for x in value) else value
                )
            elif isinstance(value, dict):
                # Recursively normalize dictionaries
                normalized[key] = self._normalize_parameters(value)
            else:
                normalized[key] = str(value)

        return normalized

    async def get_cached_content(
        self,
        cache_type: CacheType,
        parameters: dict[str, Any],
        strategy: Optional[CacheStrategy] = None,
    ) -> Optional[dict[str, Any]]:
        """Retrieve cached content using specified strategy."""

        strategy = strategy or self.cache_config[cache_type]["strategy"]

        if strategy == CacheStrategy.EXACT_MATCH:
            return await self._get_exact_match(cache_type, parameters)
        elif strategy == CacheStrategy.SEMANTIC_MATCH:
            return await self._get_semantic_match(cache_type, parameters)
        elif strategy == CacheStrategy.FUZZY_MATCH:
            return await self._get_fuzzy_match(cache_type, parameters)
        elif strategy == CacheStrategy.TEMPLATE_MATCH:
            return await self._get_template_match(cache_type, parameters)

        return None

    async def _get_exact_match(
        self, cache_type: CacheType, parameters: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Get exact parameter match from cache."""
        cache_key = self._create_cache_key(cache_type, parameters)

        # Try Redis first (fast lookup)
        if self.redis_client:
            try:
                cached_data = await self.redis_client.get(cache_key)
                if cached_data:
                    result = json.loads(cached_data)
                    await self._update_cache_stats(cache_key, "redis_hit")
                    return result
            except Exception as e:
                logger.warning(f"Redis cache lookup failed: {e}")

        # Try database (persistent lookup)
        try:
            async with get_db() as db:
                cache_entry = (
                    await db.query(ContentCacheEntry)
                    .filter(
                        ContentCacheEntry.cache_key == cache_key,
                        ContentCacheEntry.is_active == True,
                        ContentCacheEntry.expires_at > datetime.utcnow(),
                    )
                    .first()
                )

                if cache_entry:
                    # Update stats
                    cache_entry.hit_count += 1
                    cache_entry.last_accessed = datetime.utcnow()
                    await db.commit()

                    # Cache in Redis for faster future access
                    if self.redis_client:
                        ttl = self.cache_config[cache_type]["ttl"]
                        await self.redis_client.setex(
                            cache_key, ttl, json.dumps(cache_entry.content_data)
                        )

                    return cache_entry.content_data
        except Exception as e:
            logger.error(f"Database cache lookup failed: {e}")

        return None

    async def _get_semantic_match(
        self, cache_type: CacheType, parameters: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Get semantically similar content from cache."""
        # For semantic matching, we look for similar concepts/prompts
        concept = parameters.get("concept", parameters.get("prompt", ""))
        age_group = parameters.get("age_group", "")

        if not concept:
            return None

        try:
            async with get_db() as db:
                # Search for similar concepts using text similarity
                similar_entries = (
                    await db.query(ContentCacheEntry)
                    .filter(
                        ContentCacheEntry.cache_type == cache_type,
                        ContentCacheEntry.is_active == True,
                        ContentCacheEntry.expires_at > datetime.utcnow(),
                        ContentCacheEntry.normalized_params["age_group"].astext
                        == age_group,
                    )
                    .limit(10)
                    .all()
                )

                # Simple similarity check (could be enhanced with vector embeddings)
                best_match = None
                best_similarity = 0.0

                for entry in similar_entries:
                    stored_concept = entry.normalized_params.get(
                        "concept", entry.normalized_params.get("prompt", "")
                    )
                    similarity = self._calculate_text_similarity(
                        concept.lower(), stored_concept.lower()
                    )

                    if (
                        similarity > best_similarity and similarity > 0.8
                    ):  # 80% similarity threshold
                        best_match = entry
                        best_similarity = similarity

                if best_match:
                    # Update stats
                    best_match.hit_count += 1
                    best_match.last_accessed = datetime.utcnow()
                    await db.commit()

                    logger.info(
                        f"Semantic cache hit with {best_similarity:.2f} similarity"
                    )
                    return best_match.content_data
        except Exception as e:
            logger.error(f"Semantic cache lookup failed: {e}")

        return None

    async def _get_fuzzy_match(
        self, cache_type: CacheType, parameters: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Get fuzzy parameter match from cache."""
        # Fuzzy matching allows for slight variations in parameters
        normalized_params = self._normalize_parameters(parameters)

        try:
            async with get_db() as db:
                similar_entries = (
                    await db.query(ContentCacheEntry)
                    .filter(
                        ContentCacheEntry.cache_type == cache_type,
                        ContentCacheEntry.is_active == True,
                        ContentCacheEntry.expires_at > datetime.utcnow(),
                    )
                    .limit(20)
                    .all()
                )

                for entry in similar_entries:
                    if self._parameters_fuzzy_match(
                        normalized_params, entry.normalized_params
                    ):
                        # Update stats
                        entry.hit_count += 1
                        entry.last_accessed = datetime.utcnow()
                        await db.commit()

                        return entry.content_data
        except Exception as e:
            logger.error(f"Fuzzy cache lookup failed: {e}")

        return None

    async def _get_template_match(
        self, cache_type: CacheType, parameters: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Get template-based match from cache."""
        # Template matching focuses on structure rather than exact content
        template_params = {
            "age_group": parameters.get("age_group"),
            "subject_area": parameters.get("subject_area"),
            "difficulty_level": parameters.get("difficulty_level"),
            "video_duration": parameters.get("video_duration"),
        }

        try:
            async with get_db() as db:
                template_entries = (
                    await db.query(ContentCacheEntry)
                    .filter(
                        ContentCacheEntry.cache_type == cache_type,
                        ContentCacheEntry.is_active == True,
                        ContentCacheEntry.expires_at > datetime.utcnow(),
                    )
                    .all()
                )

                for entry in template_entries:
                    if self._template_parameters_match(
                        template_params, entry.normalized_params
                    ):
                        # Update stats
                        entry.hit_count += 1
                        entry.last_accessed = datetime.utcnow()
                        await db.commit()

                        return entry.content_data
        except Exception as e:
            logger.error(f"Template cache lookup failed: {e}")

        return None

    async def cache_content(
        self,
        cache_type: CacheType,
        parameters: dict[str, Any],
        content: dict[str, Any],
        metadata: Optional[dict[str, Any]] = None,
        cost: Optional[str] = None,
        generation_time: Optional[int] = None,
        ai_service: Optional[str] = None,
        ai_model: Optional[str] = None,
    ) -> str:
        """Cache generated content."""

        cache_key = self._create_cache_key(cache_type, parameters)
        normalized_params = self._normalize_parameters(parameters)
        content_hash = hashlib.sha256(
            json.dumps(content, sort_keys=True).encode()
        ).hexdigest()

        ttl = self.cache_config[cache_type]["ttl"]
        expires_at = datetime.utcnow() + timedelta(seconds=ttl)

        # Cache in Redis (fast access)
        if self.redis_client:
            try:
                await self.redis_client.setex(cache_key, ttl, json.dumps(content))
            except Exception as e:
                logger.warning(f"Failed to cache in Redis: {e}")

        # Cache in database (persistent)
        try:
            async with get_db() as db:
                cache_entry = ContentCacheEntry(
                    cache_key=cache_key,
                    content_hash=content_hash,
                    cache_type=cache_type,
                    content_type=self._determine_content_type(content),
                    input_parameters=parameters,
                    normalized_params=normalized_params,
                    content_data=content,
                    metadata=metadata or {},
                    generation_cost=cost,
                    generation_time=generation_time,
                    ai_service=ai_service,
                    ai_model=ai_model,
                    expires_at=expires_at,
                )

                db.add(cache_entry)
                await db.commit()

                logger.info(f"Cached {cache_type} content with key {cache_key}")

        except Exception as e:
            logger.error(f"Failed to cache in database: {e}")

        return cache_key

    def _determine_content_type(self, content: dict[str, Any]) -> str:
        """Determine content type from content structure."""
        if "text" in content:
            return "text"
        elif "image_url" in content:
            return "image_url"
        elif "audio_url" in content:
            return "audio_url"
        elif "video_url" in content:
            return "video_url"
        elif "questions" in content:
            return "quiz_questions"
        else:
            return "mixed"

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity (could be enhanced with embeddings)."""
        words1 = set(text1.split())
        words2 = set(text2.split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def _parameters_fuzzy_match(
        self, params1: dict[str, Any], params2: dict[str, Any]
    ) -> bool:
        """Check if parameters fuzzy match."""
        # Must match on key parameters
        key_params = ["age_group", "subject_area"]

        for key in key_params:
            if params1.get(key) != params2.get(key):
                return False

        # Allow fuzzy matching on other parameters
        fuzzy_params = ["difficulty_level", "duration"]
        fuzzy_threshold = 0.8

        matches = 0
        total = 0

        for key in fuzzy_params:
            if key in params1 and key in params2:
                total += 1
                val1, val2 = params1[key], params2[key]

                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    # Numeric fuzzy matching
                    if val1 == 0 or val2 == 0:
                        similarity = 1.0 if val1 == val2 else 0.0
                    else:
                        similarity = 1 - abs(val1 - val2) / max(val1, val2)
                else:
                    # String fuzzy matching
                    similarity = self._calculate_text_similarity(str(val1), str(val2))

                if similarity >= fuzzy_threshold:
                    matches += 1

        return total == 0 or (matches / total) >= fuzzy_threshold

    def _template_parameters_match(
        self, template_params: dict[str, Any], stored_params: dict[str, Any]
    ) -> bool:
        """Check if template parameters match."""
        for key, value in template_params.items():
            if value is not None and stored_params.get(key) != value:
                return False
        return True

    async def _update_cache_stats(self, cache_key: str, stat_type: str):
        """Update cache statistics."""
        try:
            async with get_db() as db:
                cache_entry = (
                    await db.query(ContentCacheEntry)
                    .filter(ContentCacheEntry.cache_key == cache_key)
                    .first()
                )

                if cache_entry:
                    cache_entry.hit_count += 1
                    cache_entry.last_accessed = datetime.utcnow()
                    await db.commit()
        except Exception as e:
            logger.error(f"Failed to update cache stats: {e}")

    async def cleanup_expired_cache(self):
        """Clean up expired cache entries."""
        try:
            async with get_db() as db:
                expired_count = (
                    await db.query(ContentCacheEntry)
                    .filter(ContentCacheEntry.expires_at < datetime.utcnow())
                    .delete()
                )

                await db.commit()
                logger.info(f"Cleaned up {expired_count} expired cache entries")
        except Exception as e:
            logger.error(f"Cache cleanup failed: {e}")

    async def get_cache_statistics(self) -> dict[str, Any]:
        """Get cache statistics."""
        try:
            async with get_db() as db:
                stats = {
                    "total_entries": await db.query(ContentCacheEntry).count(),
                    "active_entries": await db.query(ContentCacheEntry)
                    .filter(
                        ContentCacheEntry.is_active == True,
                        ContentCacheEntry.expires_at > datetime.utcnow(),
                    )
                    .count(),
                    "total_hits": await db.query(
                        db.func.sum(ContentCacheEntry.hit_count)
                    ).scalar()
                    or 0,
                    "cache_by_type": {},
                }

                for cache_type in CacheType:
                    type_count = (
                        await db.query(ContentCacheEntry)
                        .filter(
                            ContentCacheEntry.cache_type == cache_type,
                            ContentCacheEntry.is_active == True,
                        )
                        .count()
                    )
                    stats["cache_by_type"][cache_type] = type_count

                return stats
        except Exception as e:
            logger.error(f"Failed to get cache statistics: {e}")
            return {}


# Global cache manager instance
content_cache = ContentCacheManager()


# Convenience functions
async def get_cached_script(concept: str, age_group: str, **kwargs) -> Optional[str]:
    """Get cached script content."""
    parameters = {"concept": concept, "age_group": age_group, **kwargs}
    cached = await content_cache.get_cached_content(CacheType.SCRIPT, parameters)
    return cached.get("text") if cached else None


async def cache_script(concept: str, age_group: str, text: str, **kwargs) -> str:
    """Cache script content."""
    parameters = {"concept": concept, "age_group": age_group, **kwargs}
    content = {"text": text}
    return await content_cache.cache_content(
        CacheType.SCRIPT, parameters, content, **kwargs
    )


async def get_cached_image(prompt: str, **kwargs) -> Optional[str]:
    """Get cached image URL."""
    parameters = {"prompt": prompt, **kwargs}
    cached = await content_cache.get_cached_content(CacheType.IMAGE, parameters)
    return cached.get("image_url") if cached else None


async def cache_image(prompt: str, image_url: str, **kwargs) -> str:
    """Cache image content."""
    parameters = {"prompt": prompt, **kwargs}
    content = {"image_url": image_url}
    return await content_cache.cache_content(
        CacheType.IMAGE, parameters, content, **kwargs
    )
