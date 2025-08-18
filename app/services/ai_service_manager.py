"""
AI Service Manager with fallback handling and mocking capabilities
"""

import asyncio
import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional

import structlog

from app.core.config import ai_config, settings

logger = structlog.get_logger()


class ServiceTier(str, Enum):
    """Service tier enumeration."""

    PREMIUM = "premium"
    STANDARD = "standard"
    BUDGET = "budget"


class ServiceType(str, Enum):
    """AI service type enumeration."""

    TEXT_GENERATION = "text_generation"
    IMAGE_GENERATION = "image_generation"
    VOICE_SYNTHESIS = "voice_synthesis"
    VIDEO_GENERATION = "video_generation"
    MUSIC_GENERATION = "music_generation"
    AVATAR_GENERATION = "avatar_generation"


class AIServiceError(Exception):
    """Base exception for AI service errors."""

    pass


class ServiceUnavailableError(AIServiceError):
    """Exception raised when a service is unavailable."""

    pass


class QuotaExceededError(AIServiceError):
    """Exception raised when service quota is exceeded."""

    pass


class BaseAIService(ABC):
    """Base class for all AI services."""

    def __init__(
        self, service_name: str, api_key: Optional[str] = None, mock_mode: bool = False
    ):
        self.service_name = service_name
        self.api_key = api_key
        self.mock_mode = mock_mode or settings.ENVIRONMENT == "test"
        self.is_available = True
        self.last_error = None

    @abstractmethod
    async def generate(self, **kwargs) -> dict[str, Any]:
        """Generate content using the AI service."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the service is healthy."""
        pass

    async def mock_generate(self, **kwargs) -> dict[str, Any]:
        """Mock generation for testing."""
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate API latency
        return self._create_mock_response(**kwargs)

    @abstractmethod
    def _create_mock_response(self, **kwargs) -> dict[str, Any]:
        """Create a mock response for testing."""
        pass


class TextGenerationService(BaseAIService):
    """Text generation service (OpenAI, Anthropic)."""

    async def generate(
        self, prompt: str, model: str = "gpt-4", **kwargs
    ) -> dict[str, Any]:
        """Generate text content."""
        if self.mock_mode:
            return await self.mock_generate(prompt=prompt, model=model, **kwargs)

        if self.service_name == "openai":
            return await self._openai_generate(prompt, model, **kwargs)
        elif self.service_name == "anthropic":
            return await self._anthropic_generate(prompt, model, **kwargs)
        else:
            raise AIServiceError(
                f"Unknown text generation service: {self.service_name}"
            )

    async def _openai_generate(
        self, prompt: str, model: str, **kwargs
    ) -> dict[str, Any]:
        """Generate text using OpenAI."""
        try:
            import openai

            client = openai.AsyncOpenAI(api_key=self.api_key)

            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", 2000),
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 0.9),
            )

            return {
                "text": response.choices[0].message.content,
                "model": model,
                "usage": response.usage.dict() if response.usage else {},
                "service": "openai",
            }
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise AIServiceError(f"OpenAI generation failed: {e}")

    async def _anthropic_generate(
        self, prompt: str, model: str, **kwargs
    ) -> dict[str, Any]:
        """Generate text using Anthropic."""
        try:
            import anthropic

            client = anthropic.AsyncAnthropic(api_key=self.api_key)

            response = await client.messages.create(
                model=model,
                max_tokens=kwargs.get("max_tokens", 2000),
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
            )

            return {
                "text": response.content[0].text,
                "model": model,
                "usage": response.usage.dict() if hasattr(response, "usage") else {},
                "service": "anthropic",
            }
        except Exception as e:
            logger.error(f"Anthropic generation failed: {e}")
            raise AIServiceError(f"Anthropic generation failed: {e}")

    async def health_check(self) -> bool:
        """Check service health."""
        if self.mock_mode:
            return True

        try:
            # Simple health check with minimal token usage
            result = await self.generate("Hello", max_tokens=1)
            return bool(result.get("text"))
        except Exception:
            return False

    def _create_mock_response(self, **kwargs) -> dict[str, Any]:
        """Create mock text response."""
        prompt = kwargs.get("prompt", "")
        mock_responses = [
            "This is a mock educational script about photosynthesis...",
            "Here's an engaging explanation of gravity for 12-year-olds...",
            "Let's explore the fascinating world of DNA structure...",
        ]

        return {
            "text": random.choice(mock_responses),
            "model": kwargs.get("model", "mock-gpt-4"),
            "usage": {
                "prompt_tokens": len(prompt),
                "completion_tokens": 150,
                "total_tokens": len(prompt) + 150,
            },
            "service": f"mock-{self.service_name}",
        }


class ImageGenerationService(BaseAIService):
    """Image generation service (DALL-E, Midjourney, Stable Diffusion)."""

    async def generate(self, prompt: str, **kwargs) -> dict[str, Any]:
        """Generate image content."""
        if self.mock_mode:
            return await self.mock_generate(prompt=prompt, **kwargs)

        if self.service_name == "dall-e-3":
            return await self._dalle_generate(prompt, **kwargs)
        else:
            # Placeholder for other image services
            raise AIServiceError(
                f"Image service {self.service_name} not implemented yet"
            )

    async def _dalle_generate(self, prompt: str, **kwargs) -> dict[str, Any]:
        """Generate image using DALL-E."""
        try:
            import openai

            client = openai.AsyncOpenAI(api_key=self.api_key)

            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=kwargs.get("size", "1024x1792"),
                quality=kwargs.get("quality", "standard"),
                n=1,
            )

            return {
                "image_url": response.data[0].url,
                "revised_prompt": response.data[0].revised_prompt,
                "service": "dall-e-3",
            }
        except Exception as e:
            logger.error(f"DALL-E generation failed: {e}")
            raise AIServiceError(f"DALL-E generation failed: {e}")

    async def health_check(self) -> bool:
        """Check service health."""
        if self.mock_mode:
            return True
        return True  # Implement actual health check

    def _create_mock_response(self, **kwargs) -> dict[str, Any]:
        """Create mock image response."""
        return {
            "image_url": f"https://mock-images.example.com/{random.randint(1000, 9999)}.jpg",
            "revised_prompt": kwargs.get("prompt", "mock image"),
            "service": f"mock-{self.service_name}",
        }


class VoiceSynthesisService(BaseAIService):
    """Voice synthesis service (ElevenLabs, Azure, Google)."""

    async def generate(self, text: str, voice_id: str, **kwargs) -> dict[str, Any]:
        """Generate voice audio."""
        if self.mock_mode:
            return await self.mock_generate(text=text, voice_id=voice_id, **kwargs)

        if self.service_name == "elevenlabs":
            return await self._elevenlabs_generate(text, voice_id, **kwargs)
        else:
            raise AIServiceError(
                f"Voice service {self.service_name} not implemented yet"
            )

    async def _elevenlabs_generate(
        self, text: str, voice_id: str, **kwargs
    ) -> dict[str, Any]:
        """Generate voice using ElevenLabs."""
        try:
            # Placeholder for ElevenLabs integration
            # Would use elevenlabs library here
            return {
                "audio_url": f"https://mock-audio.example.com/{random.randint(1000, 9999)}.mp3",
                "duration": len(text) * 0.1,  # Rough duration estimate
                "service": "elevenlabs",
            }
        except Exception as e:
            logger.error(f"ElevenLabs generation failed: {e}")
            raise AIServiceError(f"ElevenLabs generation failed: {e}")

    async def health_check(self) -> bool:
        """Check service health."""
        if self.mock_mode:
            return True
        return True

    def _create_mock_response(self, **kwargs) -> dict[str, Any]:
        """Create mock voice response."""
        text = kwargs.get("text", "")
        return {
            "audio_url": f"https://mock-audio.example.com/{random.randint(1000, 9999)}.mp3",
            "duration": len(text) * 0.1,
            "service": f"mock-{self.service_name}",
        }


class AIServiceManager:
    """Manager for all AI services with fallback handling and mocking."""

    def __init__(self, mock_mode: bool = False):
        self.mock_mode = mock_mode or settings.ENVIRONMENT == "test"
        self.services: dict[str, dict[str, BaseAIService]] = {}
        self.service_health: dict[str, bool] = {}
        self._initialize_services()

    def _initialize_services(self):
        """Initialize all AI services."""

        # Text Generation Services
        self.services[ServiceType.TEXT_GENERATION] = {
            "openai": TextGenerationService(
                "openai", settings.OPENAI_API_KEY, self.mock_mode
            ),
            "anthropic": TextGenerationService(
                "anthropic", settings.ANTHROPIC_API_KEY, self.mock_mode
            ),
        }

        # Image Generation Services
        self.services[ServiceType.IMAGE_GENERATION] = {
            "dall-e-3": ImageGenerationService(
                "dall-e-3", settings.OPENAI_API_KEY, self.mock_mode
            ),
            "midjourney": ImageGenerationService(
                "midjourney", settings.MIDJOURNEY_API_KEY, self.mock_mode
            ),
            "stable-diffusion": ImageGenerationService(
                "stable-diffusion", settings.STABLE_DIFFUSION_API_KEY, self.mock_mode
            ),
        }

        # Voice Synthesis Services
        self.services[ServiceType.VOICE_SYNTHESIS] = {
            "elevenlabs": VoiceSynthesisService(
                "elevenlabs", settings.ELEVENLABS_API_KEY, self.mock_mode
            ),
            "azure": VoiceSynthesisService(
                "azure", settings.AZURE_SPEECH_KEY, self.mock_mode
            ),
            "google": VoiceSynthesisService(
                "google", settings.GOOGLE_CLOUD_TTS_KEY, self.mock_mode
            ),
        }

    async def generate_content(
        self,
        service_type: ServiceType,
        tier: ServiceTier = ServiceTier.PREMIUM,
        **kwargs,
    ) -> dict[str, Any]:
        """Generate content with automatic fallback handling."""

        service_config = self._get_service_config(service_type, tier)
        primary_service = service_config["service"]
        fallback_service = service_config.get("fallback")

        # Try primary service
        try:
            service = self.services[service_type][primary_service]
            result = await service.generate(**kwargs)
            result["service_used"] = primary_service
            result["tier"] = tier
            return result
        except (AIServiceError, ServiceUnavailableError, QuotaExceededError) as e:
            logger.warning(f"Primary service {primary_service} failed: {e}")

            # Try fallback service if available
            if fallback_service and fallback_service in self.services[service_type]:
                try:
                    service = self.services[service_type][fallback_service]
                    result = await service.generate(**kwargs)
                    result["service_used"] = fallback_service
                    result["tier"] = tier
                    result["fallback_used"] = True
                    return result
                except Exception as fallback_error:
                    logger.error(
                        f"Fallback service {fallback_service} also failed: {fallback_error}"
                    )

            raise AIServiceError(f"All services failed for {service_type}")

    def _get_service_config(
        self, service_type: ServiceType, tier: ServiceTier
    ) -> dict[str, Any]:
        """Get service configuration for given type and tier."""

        config_map = {
            ServiceType.TEXT_GENERATION: ai_config.TEXT_GENERATION_SERVICES,
            ServiceType.IMAGE_GENERATION: ai_config.IMAGE_GENERATION_SERVICES,
            ServiceType.VOICE_SYNTHESIS: ai_config.VOICE_SYNTHESIS_SERVICES,
            ServiceType.VIDEO_GENERATION: ai_config.VIDEO_GENERATION_SERVICES,
            ServiceType.MUSIC_GENERATION: ai_config.MUSIC_GENERATION_SERVICES,
            ServiceType.AVATAR_GENERATION: ai_config.AVATAR_GENERATION_SERVICES,
        }

        service_configs = config_map.get(service_type, {})
        return service_configs.get(tier, service_configs.get(ServiceTier.PREMIUM, {}))

    async def health_check_all(self) -> dict[str, dict[str, bool]]:
        """Check health of all services."""
        health_results = {}

        for service_type, services in self.services.items():
            health_results[service_type] = {}

            for service_name, service in services.items():
                try:
                    is_healthy = await service.health_check()
                    health_results[service_type][service_name] = is_healthy
                    self.service_health[f"{service_type}.{service_name}"] = is_healthy
                except Exception as e:
                    logger.error(f"Health check failed for {service_name}: {e}")
                    health_results[service_type][service_name] = False
                    self.service_health[f"{service_type}.{service_name}"] = False

        return health_results

    def get_service_status(self) -> dict[str, Any]:
        """Get status of all services."""
        return {
            "mock_mode": self.mock_mode,
            "environment": settings.ENVIRONMENT,
            "service_health": self.service_health,
            "available_services": {
                service_type: list(services.keys())
                for service_type, services in self.services.items()
            },
        }

    def enable_mock_mode(self):
        """Enable mock mode for all services."""
        self.mock_mode = True
        for service_type in self.services:
            for service in self.services[service_type].values():
                service.mock_mode = True

    def disable_mock_mode(self):
        """Disable mock mode for all services."""
        self.mock_mode = False
        for service_type in self.services:
            for service in self.services[service_type].values():
                service.mock_mode = False


# Global service manager instance
ai_service_manager = AIServiceManager(mock_mode=settings.ENVIRONMENT == "test")


# Convenience functions for common operations
async def generate_script(prompt: str, age_group: str, **kwargs) -> str:
    """Generate educational script."""
    result = await ai_service_manager.generate_content(
        ServiceType.TEXT_GENERATION,
        ServiceTier.PREMIUM,
        prompt=prompt,
        age_group=age_group,
        **kwargs,
    )
    return result["text"]


async def generate_image(prompt: str, **kwargs) -> str:
    """Generate educational image."""
    result = await ai_service_manager.generate_content(
        ServiceType.IMAGE_GENERATION, ServiceTier.PREMIUM, prompt=prompt, **kwargs
    )
    return result["image_url"]


async def generate_voice(text: str, age_group: str, **kwargs) -> str:
    """Generate voice narration."""
    # Get voice configuration for age group
    voice_config = ai_config.VOICE_SYNTHESIS_SERVICES["premium"]["voices"].get(
        age_group, {}
    )
    voice_id = voice_config.get("voice_id", "default")

    result = await ai_service_manager.generate_content(
        ServiceType.VOICE_SYNTHESIS,
        ServiceTier.PREMIUM,
        text=text,
        voice_id=voice_id,
        **voice_config,
        **kwargs,
    )
    return result["audio_url"]
