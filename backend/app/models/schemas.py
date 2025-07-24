from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Query Models
class QueryRequest(BaseModel):
    """Request model for user queries"""
    query: str = Field(..., description="The user's question or query")
    max_results: int = Field(default=5, description="Maximum number of results to return")
    include_graph_context: bool = Field(default=True, description="Whether to include graph relationships")

class QueryResponse(BaseModel):
    """Response model for query results"""
    answer: str = Field(..., description="The generated answer")
    sources: List[Dict[str, Any]] = Field(default=[], description="Source documents and context")
    graph_context: Optional[Dict[str, Any]] = Field(default=None, description="Graph relationships found")
    confidence_score: float = Field(..., description="Confidence score of the answer")
    processing_time: float = Field(..., description="Time taken to process the query")

# Document Models
class DocumentUpload(BaseModel):
    """Model for document upload"""
    content: str = Field(..., description="Document content")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Document metadata")
    document_type: str = Field(default="text", description="Type of document")

class DocumentResponse(BaseModel):
    """Response model for document operations"""
    id: str = Field(..., description="Document ID")
    status: str = Field(..., description="Processing status")
    message: str = Field(..., description="Status message")

# Graph Models
class Entity(BaseModel):
    """Model for graph entities"""
    id: str = Field(..., description="Entity ID")
    name: str = Field(..., description="Entity name")
    type: str = Field(..., description="Entity type")
    properties: Optional[Dict[str, Any]] = Field(default={}, description="Entity properties")

class Relationship(BaseModel):
    """Model for graph relationships"""
    source_id: str = Field(..., description="Source entity ID")
    target_id: str = Field(..., description="Target entity ID")
    relationship_type: str = Field(..., description="Type of relationship")
    properties: Optional[Dict[str, Any]] = Field(default={}, description="Relationship properties")

class GraphContext(BaseModel):
    """Model for graph context in responses"""
    entities: List[Entity] = Field(default=[], description="Relevant entities")
    relationships: List[Relationship] = Field(default=[], description="Relevant relationships")
    subgraph: Optional[Dict[str, Any]] = Field(default=None, description="Subgraph data")

# Health and Status Models
class ServiceStatus(BaseModel):
    """Model for service health status"""
    service: str = Field(..., description="Service name")
    status: str = Field(..., description="Service status")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional details")

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Overall system status")
    services: Dict[str, ServiceStatus] = Field(..., description="Individual service statuses")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp") 