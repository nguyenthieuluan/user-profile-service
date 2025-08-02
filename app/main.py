from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.routes import router
from app.db import init_db
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="User Profile Service",
    description="FastAPI user profile microservice with PostgreSQL and Podman",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    logger.info("Starting User Profile Service...")
    init_db()
    logger.info("Database initialized successfully")

app.include_router(router)
