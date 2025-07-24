// API Types matching our FastAPI schemas

export interface QueryRequest {
  query: string;
  max_results?: number;
  include_graph_context?: boolean;
}

export interface QueryResponse {
  answer: string;
  sources: Source[];
  graph_context?: GraphContext;
  confidence_score: number;
  processing_time: number;
}

export interface Source {
  content: string;
  metadata?: Record<string, unknown>;
  distance?: number;
}

export interface GraphContext {
  entities: Entity[];
  relationships: Relationship[];
  subgraph?: Record<string, unknown>;
}

export interface Entity {
  id: string;
  name: string;
  type: string;
  properties?: Record<string, unknown>;
}

export interface Relationship {
  source_id: string;
  target_id: string;
  relationship_type: string;
  properties?: Record<string, unknown>;
}

export interface DocumentUpload {
  content: string;
  metadata?: Record<string, unknown>;
  document_type?: string;
}

export interface DocumentResponse {
  id: string;
  status: string;
  message: string;
}

export interface ServiceStatus {
  service: string;
  status: string;
  details?: Record<string, unknown>;
}

export interface HealthResponse {
  status: string;
  services: Record<string, ServiceStatus>;
  timestamp: string;
  details?: {
    chroma: Record<string, unknown>;
    neo4j: Record<string, unknown>;
  };
} 