"""
AI Cost Tracking and Approval System
"""

import asyncio
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import structlog
from app.core.database import get_db
from app.core.config import settings
from app.models.billing import (
    AIServiceCost,
    AIServiceType,
    ApprovalRequest,
    ApprovalStatus,
    CostTier,
    CreatorBudget,
)

logger = structlog.get_logger()


class CostTracker:
    """Main cost tracking and approval system."""
    
    # Service cost rates (USD per unit)
    SERVICE_RATES = {
        AIServiceType.OPENAI_GPT: {
            "gpt-4": {"input": 0.03 / 1000, "output": 0.06 / 1000},  # per token
            "gpt-3.5-turbo": {"input": 0.001 / 1000, "output": 0.002 / 1000}
        },
        AIServiceType.OPENAI_DALLE: {
            "dall-e-3": {"standard": 0.040, "hd": 0.080},  # per image
            "dall-e-2": {"1024x1024": 0.020, "512x512": 0.018}
        },
        AIServiceType.ANTHROPIC_CLAUDE: {
            "claude-3-sonnet": {"input": 0.003 / 1000, "output": 0.015 / 1000},
            "claude-3-haiku": {"input": 0.00025 / 1000, "output": 0.00125 / 1000}
        },
        AIServiceType.ELEVENLABS_TTS: {
            "default": 0.18 / 1000  # per character
        },
        AIServiceType.RUNWAY_VIDEO: {
            "gen-2": 0.0125  # per second
        }
    }
    
    # Cost tier thresholds
    COST_TIERS = {
        CostTier.LOW: (0, 1.0),
        CostTier.MEDIUM: (1.0, 10.0),
        CostTier.HIGH: (10.0, 100.0),
        CostTier.CRITICAL: (100.0, float('inf'))
    }
    
    def __init__(self):
        self.approval_callbacks: Dict[str, callable] = {}
    
    def register_approval_callback(self, callback_name: str, callback: callable):
        """Register callback for approval notifications."""
        self.approval_callbacks[callback_name] = callback
    
    async def estimate_cost(
        self, 
        service_type: AIServiceType, 
        model: str, 
        operation_params: Dict[str, Any]
    ) -> Decimal:
        """Estimate cost for an AI operation."""
        
        service_rates = self.SERVICE_RATES.get(service_type, {})
        model_rates = service_rates.get(model, service_rates.get("default", {}))
        
        if not model_rates:
            logger.warning(f"No cost rates found for {service_type}:{model}")
            return Decimal("0.10")  # Default conservative estimate
        
        estimated_cost = Decimal("0.00")
        
        if service_type == AIServiceType.OPENAI_GPT:
            input_tokens = operation_params.get("input_tokens", 0)
            output_tokens = operation_params.get("max_tokens", 150)
            
            estimated_cost = (
                Decimal(str(input_tokens)) * Decimal(str(model_rates["input"])) +
                Decimal(str(output_tokens)) * Decimal(str(model_rates["output"]))
            )
        
        elif service_type == AIServiceType.OPENAI_DALLE:
            image_count = operation_params.get("n", 1)
            quality = operation_params.get("quality", "standard")
            rate = model_rates.get(quality, model_rates.get("standard", 0.040))
            estimated_cost = Decimal(str(image_count)) * Decimal(str(rate))
        
        elif service_type == AIServiceType.ELEVENLABS_TTS:
            character_count = len(operation_params.get("text", ""))
            estimated_cost = Decimal(str(character_count)) * Decimal(str(model_rates))
        
        elif service_type == AIServiceType.RUNWAY_VIDEO:
            duration = operation_params.get("duration", 5)  # seconds
            estimated_cost = Decimal(str(duration)) * Decimal(str(model_rates))
        
        return estimated_cost.quantize(Decimal("0.0001"))
    
    def determine_cost_tier(self, cost: Decimal) -> CostTier:
        """Determine cost tier based on amount."""
        cost_float = float(cost)
        
        for tier, (min_cost, max_cost) in self.COST_TIERS.items():
            if min_cost <= cost_float < max_cost:
                return tier
        
        return CostTier.CRITICAL
    
    async def check_budget_limits(self, creator_id: str, estimated_cost: Decimal) -> Dict[str, Any]:
        """Check if operation is within budget limits."""
        
        async with get_db() as db:
            budget = await db.query(CreatorBudget).filter(
                CreatorBudget.creator_id == creator_id
            ).first()
            
            if not budget:
                # Create default budget for new creator
                budget = await self._create_default_budget(creator_id, db)
            
            # Check if budget periods need reset
            await self._reset_budget_periods_if_needed(budget, db)
            
            # Calculate new totals with this operation
            new_daily = budget.daily_spent + estimated_cost
            new_weekly = budget.weekly_spent + estimated_cost
            new_monthly = budget.monthly_spent + estimated_cost
            
            # Check limits
            within_limits = (
                new_daily <= budget.daily_limit and
                new_weekly <= budget.weekly_limit and
                new_monthly <= budget.monthly_limit and
                not budget.is_suspended
            )
            
            return {
                "within_limits": within_limits,
                "daily_remaining": budget.daily_limit - new_daily,
                "weekly_remaining": budget.weekly_limit - new_weekly,
                "monthly_remaining": budget.monthly_limit - new_monthly,
                "auto_approve": estimated_cost <= budget.auto_approve_threshold,
                "requires_approval": estimated_cost >= budget.require_approval_above,
                "budget": budget
            }
    
    async def request_approval(
        self,
        creator_id: str,
        service_type: AIServiceType,
        model: str,
        operation_params: Dict[str, Any],
        project_id: Optional[str] = None,
        content_type: str = "unknown"
    ) -> Dict[str, Any]:
        """Request approval for an AI operation."""
        
        # Estimate cost
        estimated_cost = await self.estimate_cost(service_type, model, operation_params)
        cost_tier = self.determine_cost_tier(estimated_cost)
        
        # Check budget
        budget_check = await self.check_budget_limits(creator_id, estimated_cost)
        
        async with get_db() as db:
            # Create cost entry
            cost_entry = AIServiceCost(
                service_type=service_type,
                service_model=model,
                operation_type=operation_params.get("operation_type", "generation"),
                estimated_cost=estimated_cost,
                cost_tier=cost_tier,
                request_parameters=operation_params,
                project_id=project_id,
                creator_id=creator_id,
                content_type=content_type,
                approval_status=ApprovalStatus.PENDING,
                requires_approval=not budget_check["auto_approve"]
            )
            
            db.add(cost_entry)
            await db.flush()  # Get the ID
            
            # Determine approval status
            if not budget_check["within_limits"]:
                cost_entry.approval_status = ApprovalStatus.REJECTED
                cost_entry.rejection_reason = "Budget limits exceeded"
                approval_request = None
            
            elif budget_check["auto_approve"] and cost_tier in [CostTier.LOW]:
                cost_entry.approval_status = ApprovalStatus.AUTO_APPROVED
                cost_entry.approved_at = datetime.utcnow()
                cost_entry.requires_approval = False
                approval_request = None
            
            else:
                # Create approval request
                approval_request = ApprovalRequest(
                    cost_entry_id=cost_entry.id,
                    creator_id=creator_id,
                    operation_description=self._create_operation_description(
                        service_type, model, operation_params
                    ),
                    estimated_cost=estimated_cost,
                    cost_tier=cost_tier,
                    expires_at=datetime.utcnow() + timedelta(hours=24)  # 24-hour expiration
                )
                db.add(approval_request)
            
            await db.commit()
            
            # Send approval notifications if needed
            if approval_request:
                await self._send_approval_notification(approval_request)
            
            return {
                "cost_entry_id": str(cost_entry.id),
                "estimated_cost": float(estimated_cost),
                "cost_tier": cost_tier,
                "approval_status": cost_entry.approval_status,
                "requires_approval": cost_entry.requires_approval,
                "approval_request_id": str(approval_request.id) if approval_request else None,
                "budget_check": budget_check
            }
    
    async def approve_request(
        self, 
        approval_request_id: str, 
        approved_by: str,
        approval_notes: Optional[str] = None
    ) -> bool:
        """Approve an AI operation request."""
        
        async with get_db() as db:
            approval_request = await db.query(ApprovalRequest).filter(
                ApprovalRequest.id == approval_request_id,
                ApprovalRequest.status == ApprovalStatus.PENDING
            ).first()
            
            if not approval_request:
                return False
            
            # Check if not expired
            if approval_request.expires_at < datetime.utcnow():
                approval_request.status = ApprovalStatus.EXPIRED
                await db.commit()
                return False
            
            # Update approval request
            approval_request.status = ApprovalStatus.APPROVED
            approval_request.approved_by = approved_by
            approval_request.approved_at = datetime.utcnow()
            approval_request.approval_notes = approval_notes
            approval_request.approval_method = "manual"
            
            # Update cost entry
            cost_entry = await db.query(AIServiceCost).filter(
                AIServiceCost.id == approval_request.cost_entry_id
            ).first()
            
            if cost_entry:
                cost_entry.approval_status = ApprovalStatus.APPROVED
                cost_entry.approved_by = approved_by
                cost_entry.approved_at = datetime.utcnow()
            
            await db.commit()
            
            logger.info(f"Approved AI operation {approval_request_id} by {approved_by}")
            return True
    
    async def reject_request(
        self, 
        approval_request_id: str, 
        rejected_by: str,
        rejection_reason: str
    ) -> bool:
        """Reject an AI operation request."""
        
        async with get_db() as db:
            approval_request = await db.query(ApprovalRequest).filter(
                ApprovalRequest.id == approval_request_id,
                ApprovalRequest.status == ApprovalStatus.PENDING
            ).first()
            
            if not approval_request:
                return False
            
            # Update approval request
            approval_request.status = ApprovalStatus.REJECTED
            approval_request.rejection_reason = rejection_reason
            
            # Update cost entry
            cost_entry = await db.query(AIServiceCost).filter(
                AIServiceCost.id == approval_request.cost_entry_id
            ).first()
            
            if cost_entry:
                cost_entry.approval_status = ApprovalStatus.REJECTED
                cost_entry.rejection_reason = rejection_reason
            
            await db.commit()
            
            logger.info(f"Rejected AI operation {approval_request_id} by {rejected_by}")
            return True
    
    async def record_actual_cost(
        self, 
        cost_entry_id: str, 
        actual_cost: Decimal,
        usage_metrics: Dict[str, Any]
    ):
        """Record actual cost after operation completion."""
        
        async with get_db() as db:
            cost_entry = await db.query(AIServiceCost).filter(
                AIServiceCost.id == cost_entry_id
            ).first()
            
            if cost_entry:
                cost_entry.actual_cost = actual_cost
                cost_entry.tokens_used = usage_metrics.get("tokens_used")
                cost_entry.characters_processed = usage_metrics.get("characters_processed")
                cost_entry.duration_seconds = usage_metrics.get("duration_seconds")
                cost_entry.image_count = usage_metrics.get("image_count")
                cost_entry.video_duration = usage_metrics.get("video_duration")
                cost_entry.is_processed = True
                cost_entry.processing_completed_at = datetime.utcnow()
                
                # Update budget spending
                budget = await db.query(CreatorBudget).filter(
                    CreatorBudget.creator_id == cost_entry.creator_id
                ).first()
                
                if budget:
                    budget.daily_spent += actual_cost
                    budget.weekly_spent += actual_cost
                    budget.monthly_spent += actual_cost
                
                await db.commit()
    
    async def _create_default_budget(self, creator_id: str, db) -> CreatorBudget:
        """Create default budget for new creator."""
        now = datetime.utcnow()
        
        budget = CreatorBudget(
            creator_id=creator_id,
            daily_reset_at=now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
            weekly_reset_at=now + timedelta(days=(7 - now.weekday())),
            monthly_reset_at=now.replace(day=1) + timedelta(days=32)
        )
        
        db.add(budget)
        await db.commit()
        return budget
    
    async def _reset_budget_periods_if_needed(self, budget: CreatorBudget, db):
        """Reset budget periods if time has passed."""
        now = datetime.utcnow()
        
        if now >= budget.daily_reset_at:
            budget.daily_spent = Decimal("0.00")
            budget.daily_reset_at = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        if now >= budget.weekly_reset_at:
            budget.weekly_spent = Decimal("0.00")
            budget.weekly_reset_at = now + timedelta(days=(7 - now.weekday()))
        
        if now >= budget.monthly_reset_at:
            budget.monthly_spent = Decimal("0.00")
            next_month = now.replace(day=1) + timedelta(days=32)
            budget.monthly_reset_at = next_month.replace(day=1)
    
    def _create_operation_description(
        self, 
        service_type: AIServiceType, 
        model: str, 
        params: Dict[str, Any]
    ) -> str:
        """Create human-readable operation description."""
        
        descriptions = {
            AIServiceType.OPENAI_GPT: f"Generate text using {model}",
            AIServiceType.OPENAI_DALLE: f"Generate image using {model}",
            AIServiceType.ELEVENLABS_TTS: f"Generate voice narration using {model}",
            AIServiceType.RUNWAY_VIDEO: f"Generate video using {model}",
        }
        
        base_desc = descriptions.get(service_type, f"AI operation using {service_type}")
        
        if "concept" in params:
            base_desc += f" for concept: {params['concept'][:50]}..."
        elif "prompt" in params:
            base_desc += f" with prompt: {params['prompt'][:50]}..."
        
        return base_desc
    
    async def _send_approval_notification(self, approval_request: ApprovalRequest):
        """Send approval notification to relevant parties."""
        # Implement notification logic (email, webhook, etc.)
        for callback_name, callback in self.approval_callbacks.items():
            try:
                await callback(approval_request)
            except Exception as e:
                logger.error(f"Approval callback {callback_name} failed: {e}")


# Global cost tracker instance
cost_tracker = CostTracker()


# Convenience functions
async def request_ai_approval(
    creator_id: str,
    service_type: AIServiceType,
    model: str,
    operation_params: Dict[str, Any],
    **kwargs
) -> Dict[str, Any]:
    """Request approval for AI operation."""
    return await cost_tracker.request_approval(
        creator_id=creator_id,
        service_type=service_type,
        model=model,
        operation_params=operation_params,
        **kwargs
    )


async def check_operation_approved(cost_entry_id: str) -> bool:
    """Check if operation is approved."""
    async with get_db() as db:
        cost_entry = await db.query(AIServiceCost).filter(
            AIServiceCost.id == cost_entry_id
        ).first()
        
        return cost_entry and cost_entry.approval_status in [
            ApprovalStatus.APPROVED, 
            ApprovalStatus.AUTO_APPROVED
        ]