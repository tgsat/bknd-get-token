from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.token_route import router as token_router


app = FastAPI(title="ArcGIS Token Service")


app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


app.include_router(token_router, prefix="/api")