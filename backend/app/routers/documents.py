from fastapi import APIRouter, HTTPException
from typing import List
from ..models.schemas import DocumentUpload, DocumentResponse
from ..services.graph_rag_service import GraphRAGService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/documents", tags=["Documents"])

# Initialize Graph RAG service
graph_rag_service = GraphRAGService()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(document: DocumentUpload):
    """
    Upload a document to the Graph RAG system
    
    This will:
    1. Store the document in ChromaDB for semantic search
    2. Extract entities and add them to the knowledge graph
    3. Create relationships between entities
    """
    try:
        logger.info(f"Uploading document of type: {document.document_type}")
        
        # Add document to the system
        doc_id = graph_rag_service.add_document(
            content=document.content,
            metadata=document.metadata
        )
        
        logger.info(f"Document uploaded successfully with ID: {doc_id}")
        
        return DocumentResponse(
            id=doc_id,
            status="success",
            message="Document uploaded and processed successfully"
        )
        
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@router.post("/batch-upload", response_model=List[DocumentResponse])
async def batch_upload_documents(documents: List[DocumentUpload]):
    """
    Upload multiple documents in batch
    """
    try:
        logger.info(f"Batch uploading {len(documents)} documents")
        
        responses = []
        for document in documents:
            try:
                doc_id = graph_rag_service.add_document(
                    content=document.content,
                    metadata=document.metadata
                )
                
                responses.append(DocumentResponse(
                    id=doc_id,
                    status="success",
                    message="Document uploaded and processed successfully"
                ))
                
            except Exception as e:
                logger.error(f"Error processing document in batch: {e}")
                responses.append(DocumentResponse(
                    id="unknown",
                    status="error",
                    message=f"Error processing document: {str(e)}"
                ))
        
        logger.info(f"Batch upload completed. {len([r for r in responses if r.status == 'success'])} successful")
        return responses
        
    except Exception as e:
        logger.error(f"Error in batch upload: {e}")
        raise HTTPException(status_code=500, detail=f"Error in batch upload: {str(e)}")

@router.get("/stats")
async def get_document_stats():
    """Get statistics about uploaded documents"""
    try:
        from ..utils.database import get_chroma_manager, get_neo4j_manager
        
        chroma_info = get_chroma_manager().get_collection_info()
        neo4j_info = get_neo4j_manager().get_database_info()
        
        return {
            "documents": {
                "total": chroma_info.get("document_count", 0),
                "collection": chroma_info.get("name", "unknown")
            },
            "entities": {
                "total": neo4j_info.get("node_count", 0),
                "relationships": neo4j_info.get("relationship_count", 0)
            },
            "status": "healthy"
        }
        
    except Exception as e:
        logger.error(f"Error getting document stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting document stats: {str(e)}") 