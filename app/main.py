"""
MicroLearning Platform - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import structlog

from app.core.config import settings
from app.core.database import create_tables
from app.api.routes import api_router
from app.middleware.performance import PerformanceMiddleware
from app.middleware.logging import LoggingMiddleware

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI application
app = FastAPI(
    title="MicroLearning Platform API",
    description="AI-powered microlearning platform for STEM education",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_middleware(PerformanceMiddleware)
app.add_middleware(LoggingMiddleware)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Application startup event handler."""
    logger.info("Starting MicroLearning Platform API")
    
    if settings.CREATE_TABLES_ON_STARTUP:
        await create_tables()
        logger.info("Database tables created/verified")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event handler."""
    logger.info("Shutting down MicroLearning Platform API")

@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "MicroLearning Platform API",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": time.time()
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(
        "Unhandled exception occurred",
        exc_info=exc,
        path=request.url.path,
        method=request.method
    )
    
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc),
                "type": type(exc).__name__
            }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )