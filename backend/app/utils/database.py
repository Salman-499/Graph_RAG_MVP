import chromadb
from chromadb.config import Settings as ChromaSettings
from neo4j import GraphDatabase
from typing import Optional, Dict, Any
import logging
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChromaDBManager:
    """Manager for ChromaDB operations"""
    
    def __init__(self):
        self.client: Optional[chromadb.Client] = None
        self.collection: Optional[chromadb.Collection] = None
        self._initialize()
    
    def _initialize(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create ChromaDB client with persistent storage
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIRECTORY,
                settings=ChromaSettings(
                    anonymized_telemetry=False
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"ChromaDB initialized successfully. Collection: {settings.CHROMA_COLLECTION_NAME}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def add_documents(self, documents: list, metadatas: list, ids: list):
        """Add documents to ChromaDB"""
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(documents)} documents to ChromaDB")
        except Exception as e:
            logger.error(f"Failed to add documents to ChromaDB: {e}")
            raise
    
    def query(self, query_texts: list, n_results: int = 5):
        """Query ChromaDB for similar documents"""
        try:
            results = self.collection.query(
                query_texts=query_texts,
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Failed to query ChromaDB: {e}")
            raise
    
    def get_collection_info(self):
        """Get information about the collection"""
        try:
            count = self.collection.count()
            return {
                "name": settings.CHROMA_COLLECTION_NAME,
                "document_count": count,
                "status": "connected"
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {"status": "error", "error": str(e)}

class Neo4jManager:
    """Manager for Neo4j operations"""
    
    def __init__(self):
        self.driver: Optional[GraphDatabase.driver] = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Neo4j driver"""
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            
            # Test connection
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()
            
            logger.info("Neo4j initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j: {e}")
            raise
    
    def create_entity(self, entity_id: str, name: str, entity_type: str, properties: Dict[str, Any] = None):
        """Create a new entity in the graph"""
        try:
            with self.driver.session() as session:
                query = """
                MERGE (e:Entity {id: $entity_id})
                SET e.name = $name, e.type = $entity_type
                """
                if properties:
                    for key, value in properties.items():
                        query += f", e.{key} = ${key}"
                
                session.run(query, entity_id=entity_id, name=name, entity_type=entity_type, **(properties or {}))
                logger.info(f"Created entity: {name} ({entity_type})")
        except Exception as e:
            logger.error(f"Failed to create entity: {e}")
            raise
    
    def create_relationship(self, source_id: str, target_id: str, relationship_type: str, properties: Dict[str, Any] = None):
        """Create a relationship between entities"""
        try:
            with self.driver.session() as session:
                query = """
                MATCH (source:Entity {id: $source_id})
                MATCH (target:Entity {id: $target_id})
                MERGE (source)-[r:RELATES_TO {type: $relationship_type}]->(target)
                """
                if properties:
                    for key, value in properties.items():
                        query += f" SET r.{key} = ${key}"
                
                session.run(query, source_id=source_id, target_id=target_id, relationship_type=relationship_type, **(properties or {}))
                logger.info(f"Created relationship: {source_id} -[{relationship_type}]-> {target_id}")
        except Exception as e:
            logger.error(f"Failed to create relationship: {e}")
            raise
    
    def query_entities(self, entity_names: list):
        """Query for entities and their relationships"""
        try:
            with self.driver.session() as session:
                query = """
                MATCH (e:Entity)
                WHERE e.name IN $entity_names
                OPTIONAL MATCH (e)-[r:RELATES_TO]->(related:Entity)
                RETURN e, r, related
                """
                result = session.run(query, entity_names=entity_names)
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Failed to query entities: {e}")
            raise
    
    def get_database_info(self):
        """Get information about the database"""
        try:
            with self.driver.session() as session:
                # Get node count
                node_result = session.run("MATCH (n) RETURN count(n) as node_count")
                node_count = node_result.single()["node_count"]
                
                # Get relationship count
                rel_result = session.run("MATCH ()-[r]->() RETURN count(r) as rel_count")
                rel_count = rel_result.single()["rel_count"]
                
                return {
                    "node_count": node_count,
                    "relationship_count": rel_count,
                    "status": "connected"
                }
        except Exception as e:
            logger.error(f"Failed to get database info: {e}")
            return {"status": "error", "error": str(e)}
    
    def close(self):
        """Close the Neo4j driver"""
        if self.driver:
            self.driver.close()

# Global database managers
chroma_manager: Optional[ChromaDBManager] = None
neo4j_manager: Optional[Neo4jManager] = None

def initialize_databases():
    """Initialize both database managers"""
    global chroma_manager, neo4j_manager
    
    try:
        chroma_manager = ChromaDBManager()
        neo4j_manager = Neo4jManager()
        logger.info("All databases initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize databases: {e}")
        return False

def get_chroma_manager() -> ChromaDBManager:
    """Get ChromaDB manager instance"""
    if chroma_manager is None:
        raise RuntimeError("ChromaDB manager not initialized")
    return chroma_manager

def get_neo4j_manager() -> Neo4jManager:
    """Get Neo4j manager instance"""
    if neo4j_manager is None:
        raise RuntimeError("Neo4j manager not initialized")
    return neo4j_manager 