from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from ..models.schemas import QueryRequest, QueryResponse
from ..services.graph_rag_service import GraphRAGService
from ..utils.database import get_chroma_manager, get_neo4j_manager
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/query", tags=["Query"])

# Initialize Graph RAG service lazily
graph_rag_service = None

def get_graph_rag_service():
    global graph_rag_service
    if graph_rag_service is None:
        graph_rag_service = GraphRAGService()
    return graph_rag_service

@router.post("/", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a user query using Graph RAG
    
    This endpoint combines:
    1. Semantic search using ChromaDB
    2. Graph traversal using Neo4j
    3. LLM generation using OpenAI
    """
    try:
        logger.info(f"Processing query: {request.query}")
        
        # Process the query using Graph RAG
        service = get_graph_rag_service()
        response = service.process_query(
            query=request.query,
            max_results=request.max_results,
            include_graph_context=request.include_graph_context
        )
        
        logger.info(f"Query processed successfully. Confidence: {response.confidence_score}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/health")
async def query_health():
    """Health check for query service"""
    try:
        # Check if databases are accessible
        chroma_info = get_chroma_manager().get_collection_info()
        neo4j_info = get_neo4j_manager().get_database_info()
        
        return {
            "status": "healthy",
            "chroma": chroma_info,
            "neo4j": neo4j_info,
            "service": "Graph RAG Query Service"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}") 