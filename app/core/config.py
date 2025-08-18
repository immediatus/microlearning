"""
Application configuration settings
"""

from typing import Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    APP_NAME: str = "MicroLearning Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, description="Debug mode")
    ENVIRONMENT: str = Field(default="development", description="Environment name")
    SECRET_KEY: str = Field(..., description="Secret key for JWT tokens")

    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL database URL")
    DATABASE_POOL_SIZE: int = Field(
        default=20, description="Database connection pool size"
    )
    DATABASE_MAX_OVERFLOW: int = Field(default=30, description="Database max overflow")
    CREATE_TABLES_ON_STARTUP: bool = Field(
        default=True, description="Create tables on startup"
    )

    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379", description="Redis URL")
    REDIS_CACHE_TTL: int = Field(
        default=300, description="Default cache TTL in seconds"
    )

    # AI Services - Text Generation
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key for GPT models")
    OPENAI_ORG_ID: Optional[str] = Field(
        default=None, description="OpenAI organization ID"
    )
    ANTHROPIC_API_KEY: Optional[str] = Field(
        default=None, description="Anthropic Claude API key"
    )

    # AI Services - Image Generation
    DALLE_API_KEY: Optional[str] = Field(
        default=None, description="DALL-E API key (usually same as OpenAI)"
    )
    MIDJOURNEY_API_KEY: Optional[str] = Field(
        default=None, description="Midjourney API key"
    )
    STABLE_DIFFUSION_API_KEY: Optional[str] = Field(
        default=None, description="Stable Diffusion API key"
    )
    LEONARDO_AI_API_KEY: Optional[str] = Field(
        default=None, description="Leonardo AI API key"
    )

    # AI Services - Voice Synthesis
    ELEVENLABS_API_KEY: Optional[str] = Field(
        default=None, description="ElevenLabs voice synthesis API key"
    )
    AZURE_SPEECH_KEY: Optional[str] = Field(
        default=None, description="Azure Speech Services API key"
    )
    AZURE_SPEECH_REGION: Optional[str] = Field(
        default=None, description="Azure Speech Services region"
    )
    GOOGLE_CLOUD_TTS_KEY: Optional[str] = Field(
        default=None, description="Google Cloud Text-to-Speech API key"
    )

    # AI Services - Video Generation
    RUNWAY_API_KEY: Optional[str] = Field(default=None, description="RunwayML API key")
    PIKA_API_KEY: Optional[str] = Field(default=None, description="Pika Labs API key")
    STABLE_VIDEO_API_KEY: Optional[str] = Field(
        default=None, description="Stable Video Diffusion API key"
    )

    # AI Services - Music Generation
    SUNO_API_KEY: Optional[str] = Field(
        default=None, description="Suno AI music generation API key"
    )
    AIVA_API_KEY: Optional[str] = Field(
        default=None, description="AIVA music generation API key"
    )
    SOUNDRAW_API_KEY: Optional[str] = Field(
        default=None, description="Soundraw API key"
    )

    # AI Services - Avatar Generation
    DID_API_KEY: Optional[str] = Field(default=None, description="D-ID avatar API key")
    SYNTHESIA_API_KEY: Optional[str] = Field(
        default=None, description="Synthesia API key"
    )
    HEYGEN_API_KEY: Optional[str] = Field(default=None, description="HeyGen API key")

    # Storage
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, description="AWS access key")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(
        default=None, description="AWS secret key"
    )
    AWS_REGION: str = Field(default="us-east-1", description="AWS region")
    S3_BUCKET_NAME: Optional[str] = Field(
        default=None, description="S3 bucket for video storage"
    )

    # Security
    ALLOWED_HOSTS: list[str] = Field(
        default=["*"], description="Allowed hosts for CORS"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, description="Access token expiry"
    )

    # Content Generation
    MAX_CONCURRENT_GENERATIONS: int = Field(
        default=5, description="Max concurrent content generations"
    )
    CONTENT_GENERATION_TIMEOUT: int = Field(
        default=600, description="Content generation timeout in seconds"
    )

    # Video Settings
    MAX_VIDEO_DURATION: int = Field(
        default=120, description="Max video duration in seconds"
    )
    VIDEO_RESOLUTION: str = Field(
        default="1080x1920", description="Video resolution (9:16 aspect ratio)"
    )
    VIDEO_FPS: int = Field(default=30, description="Video frames per second")

    # Quiz Settings
    DEFAULT_QUIZ_TIME_LIMIT: int = Field(
        default=5000, description="Default quiz time limit in milliseconds"
    )
    MAX_QUIZ_QUESTIONS: int = Field(
        default=5, description="Maximum quiz questions per video"
    )

    # Performance
    API_RATE_LIMIT: str = Field(default="100/minute", description="API rate limit")
    MAX_REQUEST_SIZE: int = Field(
        default=10 * 1024 * 1024, description="Max request size in bytes"
    )

    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, description="Enable Prometheus metrics")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        """Parse ALLOWED_HOSTS from string if needed."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        """Validate database URL format."""
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("DATABASE_URL must be a PostgreSQL URL")
        return v

    @validator("REDIS_URL")
    def validate_redis_url(cls, v):
        """Validate Redis URL format."""
        if not v.startswith("redis://"):
            raise ValueError("REDIS_URL must be a Redis URL")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


# AI Service Configuration
class AIServiceConfig:
    """Configuration for AI services with fallback options."""

    # Text Generation Models and Fallbacks
    TEXT_GENERATION_SERVICES = {
        "primary": {"service": "openai", "model": "gpt-4", "fallback": "anthropic"},
        "fallback": {
            "service": "anthropic",
            "model": "claude-3-sonnet-20240229",
            "fallback": None,
        },
    }

    # Image Generation Services and Fallbacks
    IMAGE_GENERATION_SERVICES = {
        "primary": {
            "service": "dall-e-3",
            "model": "dall-e-3",
            "fallback": "midjourney",
        },
        "alternative": {
            "service": "midjourney",
            "model": "v6",
            "fallback": "stable-diffusion",
        },
        "budget": {"service": "stable-diffusion", "model": "xl-1.0", "fallback": None},
    }

    # Voice Synthesis Services and Configurations
    VOICE_SYNTHESIS_SERVICES = {
        "premium": {
            "service": "elevenlabs",
            "voices": {
                "12-15": {
                    "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                    "style": 0.3,
                },
                "9-11": {
                    "voice_id": "AZnzlk1XvdvUeBnXmlld",  # Domi
                    "stability": 0.7,
                    "similarity_boost": 0.8,
                    "style": 0.2,
                },
            },
            "fallback": "azure",
        },
        "standard": {
            "service": "azure",
            "voices": {"12-15": "en-US-JennyNeural", "9-11": "en-US-AriaNeural"},
            "fallback": "google",
        },
        "budget": {
            "service": "google",
            "voices": {"12-15": "en-US-Wavenet-F", "9-11": "en-US-Wavenet-E"},
            "fallback": None,
        },
    }

    # Video Generation Services
    VIDEO_GENERATION_SERVICES = {
        "premium": {"service": "runway", "model": "gen-2", "fallback": "pika"},
        "standard": {"service": "pika", "model": "v1", "fallback": "stable-video"},
        "budget": {"service": "stable-video", "model": "sv3d", "fallback": None},
    }

    # Music Generation Services
    MUSIC_GENERATION_SERVICES = {
        "premium": {"service": "suno", "model": "v3", "fallback": "aiva"},
        "standard": {"service": "aiva", "model": "pro", "fallback": "soundraw"},
        "budget": {"service": "soundraw", "model": "basic", "fallback": None},
    }

    # Avatar Generation Services
    AVATAR_GENERATION_SERVICES = {
        "premium": {"service": "synthesia", "model": "v2", "fallback": "did"},
        "standard": {"service": "did", "model": "default", "fallback": "heygen"},
        "budget": {"service": "heygen", "model": "basic", "fallback": None},
    }

    # Generation Parameters
    CONTENT_GENERATION_PARAMS = {
        "text": {
            "max_tokens": 2000,
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0.1,
        },
        "image": {
            "size": "1024x1792",  # 9:16 aspect ratio
            "quality": "standard",
            "style": "natural",
        },
        "voice": {"speed": 1.0, "pitch": 0, "volume_gain_db": 0},
        "video": {"resolution": "1080x1920", "fps": 30, "duration_max": 90},
        "music": {"duration": 60, "style": "ambient", "tempo": "medium"},
    }

    # Service Health Check Endpoints
    HEALTH_CHECK_ENDPOINTS = {
        "openai": "https://api.openai.com/v1/models",
        "anthropic": "https://api.anthropic.com/v1/messages",
        "elevenlabs": "https://api.elevenlabs.io/v1/voices",
        "runway": "https://api.runwayml.com/v1/status",
        "azure": "https://api.cognitive.microsoft.com/sts/v1.0/status",
    }


# Database Configuration
class DatabaseConfig:
    """Database configuration settings."""

    ECHO_SQL = settings.DEBUG
    POOL_SIZE = settings.DATABASE_POOL_SIZE
    MAX_OVERFLOW = settings.DATABASE_MAX_OVERFLOW
    POOL_PRE_PING = True
    POOL_RECYCLE = 3600  # 1 hour


# Redis Configuration
class RedisConfig:
    """Redis configuration settings."""

    DECODE_RESPONSES = True
    HEALTH_CHECK_INTERVAL = 30
    SOCKET_KEEPALIVE = True
    SOCKET_KEEPALIVE_OPTIONS = {
        1: 1,  # TCP_KEEPIDLE
        2: 3,  # TCP_KEEPINTVL
        3: 5,  # TCP_KEEPCNT
    }


# Export configurations
ai_config = AIServiceConfig()
db_config = DatabaseConfig()
redis_config = RedisConfig()
