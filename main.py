from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import auth, token, users
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="ArcGIS Token Management API",
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        openapi_url=settings.OPENAPI_URL,
    )
    
    # CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    application.include_router(
        auth.router,
        prefix=settings.API_V1_STR + "/auth",
        tags=["authentication"]
    )
    application.include_router(
        token.router,
        prefix=settings.API_V1_STR + "/token",
        tags=["token"]
    )
    application.include_router(
        users.router,
        prefix=settings.API_V1_STR + "/users",
        tags=["users"]
    )
    
    return application

app = create_application()

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting ArcGIS Token API")
    logger.info(f"📝 Documentation available at {settings.DOCS_URL}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Shutting down ArcGIS Token API")

@app.get("/")
async def root():
    return {
        "message": "ArcGIS Token Management API",
        "version": settings.VERSION,
        "docs": settings.DOCS_URL,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL
    )