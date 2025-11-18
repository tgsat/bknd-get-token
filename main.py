from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    application = FastAPI(
        title="ArcGIS Token API",
        description="ArcGIS Token Management Service",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return application

app = create_application()

@app.get("/")
async def root():
    return {
        "message": "ArcGIS Token Management API",
        "status": "running",
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "arcgis-token-api"}

# Import routers setelah app creation
from app.api.v1.endpoints import token, auth

app.include_router(
    token.router,
    prefix="/api/v1/token",
    tags=["token"]
)

app.include_router(
    auth.router,
    prefix="/api/v1/auth", 
    tags=["auth"]
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )