"""
FastAPI main application.
"""

import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Try to import slowapi (optional)
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    SLOWAPI_AVAILABLE = True
except ImportError:
    SLOWAPI_AVAILABLE = False
    logger.warning("slowapi not available, rate limiting disabled")

from empire_automation.api.routes import (
    agents, clients, projects, financial, leads, workflows, 
    daily_briefing, health, plan_90_day, webhooks
)
from empire_automation.api.middleware.error_handler import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)

# Initialize rate limiter (optional)
if SLOWAPI_AVAILABLE:
    try:
        limiter = Limiter(key_func=get_remote_address)
    except Exception as e:
        logger.warning(f"Rate limiter initialization failed: {e}")
        limiter = None
        SLOWAPI_AVAILABLE = False
else:
    limiter = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    logger.info("Starting Empire Automation API...")
    yield
    # Shutdown
    logger.info("Shutting down Empire Automation API...")


# Create FastAPI app
app = FastAPI(
    title="Empire Automation API",
    description="API for managing multi-entity business empire operations",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add rate limiting (if available)
if SLOWAPI_AVAILABLE and limiter:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
else:
    logger.info("Rate limiting disabled")

# Add error handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Configure CORS
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:8501,http://localhost:3000,http://127.0.0.1:8501"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Configured via CORS_ORIGINS env var
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers with API versioning
app.include_router(health.router, prefix="/api", tags=["Health"])  # Unversioned
app.include_router(daily_briefing.router, prefix="/api/v1", tags=["Daily Briefing"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(clients.router, prefix="/api/v1/clients", tags=["Clients"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(financial.router, prefix="/api/v1/financial", tags=["Financial"])
app.include_router(leads.router, prefix="/api/v1/leads", tags=["Leads"])
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["Workflows"])
app.include_router(plan_90_day.router, prefix="/api/v1/90-day-plan", tags=["90-Day Plan"])
app.include_router(webhooks.router, prefix="/api/v1", tags=["Webhooks"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Empire Automation API",
        "version": "0.1.0",
        "docs": "/docs"
    }

