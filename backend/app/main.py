from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv
import os
import logging

# Import routers
from .routers import query, documents

# Import database utilities
from .utils.database import initialize_databases
from .utils.config import settings

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Graph RAG MVP API",
    description="A Graph RAG system combining vector search and knowledge graphs",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query.router)
app.include_router(documents.router)

@app.on_event("startup")
async def startup_event():
    """Initialize databases on startup"""
    logger.info("Starting Graph RAG MVP API...")
    
    # Validate settings
    if not settings.validate():
        logger.error("Invalid settings configuration")
        return
    
    # Wait for Neo4j to be ready
    logger.info("Waiting for Neo4j to be ready...")
    import time
    import asyncio
    
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            if initialize_databases():
                logger.info("All databases initialized successfully")
                return
            else:
                logger.warning(f"Database initialization failed, retrying... ({retry_count + 1}/{max_retries})")
        except Exception as e:
            logger.warning(f"Database connection failed, retrying... ({retry_count + 1}/{max_retries}): {e}")
        
        retry_count += 1
        await asyncio.sleep(2)  # Wait 2 seconds between retries
    
    logger.error("Failed to initialize databases after maximum retries")

@app.get("/")
async def root():
    """Root endpoint to check if API is running"""
    return {"message": "Graph RAG MVP API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from .utils.database import get_chroma_manager, get_neo4j_manager
        
        chroma_info = get_chroma_manager().get_collection_info()
        neo4j_info = get_neo4j_manager().get_database_info()
        
        return {
            "status": "healthy",
            "services": {
                "api": "running",
                "chroma": chroma_info.get("status", "unknown"),
                "neo4j": neo4j_info.get("status", "unknown")
            },
            "details": {
                "chroma": chroma_info,
                "neo4j": neo4j_info
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "services": {
                "api": "running",
                "chroma": "error",
                "neo4j": "error"
            }
        }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    ) 