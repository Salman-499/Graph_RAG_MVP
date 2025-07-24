import time
import logging
from typing import List, Dict, Any, Optional, Tuple
import openai
from sentence_transformers import SentenceTransformer
import spacy
from ..utils.config import settings
from ..utils.database import get_chroma_manager, get_neo4j_manager
from ..models.schemas import QueryResponse, GraphContext, Entity, Relationship

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai.api_key = settings.OPENAI_API_KEY

class GraphRAGService:
    """Core Graph RAG service combining vector search and graph traversal"""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.nlp = spacy.load("en_core_web_sm")  # For entity extraction
        self.chroma_manager = get_chroma_manager()
        self.neo4j_manager = get_neo4j_manager()
    
    def process_query(self, query: str, max_results: int = 5, include_graph_context: bool = True) -> QueryResponse:
        """Process a user query using Graph RAG"""
        start_time = time.time()
        
        try:
            # Step 1: Extract entities from query
            entities = self._extract_entities(query)
            logger.info(f"Extracted entities: {entities}")
            
            # Step 2: Perform parallel retrieval
            semantic_results = self._semantic_search(query, max_results)
            graph_context = None
            
            if include_graph_context and entities:
                graph_context = self._graph_traversal(entities)
            
            # Step 3: Combine and format context
            combined_context = self._combine_context(semantic_results, graph_context)
            
            # Step 4: Generate answer using LLM
            answer = self._generate_answer(query, combined_context)
            
            # Step 5: Calculate confidence and processing time
            processing_time = time.time() - start_time
            confidence_score = self._calculate_confidence(semantic_results, graph_context)
            
            return QueryResponse(
                answer=answer,
                sources=semantic_results,
                graph_context=graph_context.dict() if graph_context else None,
                confidence_score=confidence_score,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text using spaCy"""
        try:
            doc = self.nlp(text)
            entities = [ent.text for ent in doc.ents]
            return entities
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return []
    
    def _semantic_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Perform semantic search using ChromaDB"""
        try:
            # Get embeddings for query
            query_embedding = self.embedding_model.encode([query])
            
            # Search in ChromaDB
            results = self.chroma_manager.query([query], n_results=max_results)
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                        'distance': results['distances'][0][i] if results['distances'] and results['distances'][0] else 0
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []
    
    def _graph_traversal(self, entities: List[str]) -> Optional[GraphContext]:
        """Traverse the knowledge graph starting from extracted entities"""
        try:
            if not entities:
                return None
            
            # Query Neo4j for entities and their relationships
            graph_data = self.neo4j_manager.query_entities(entities)
            
            # Extract entities and relationships
            found_entities = []
            found_relationships = []
            seen_entities = set()
            
            for record in graph_data:
                # Extract source entity
                if 'e' in record and record['e']:
                    entity_data = record['e']
                    entity_id = entity_data.get('id', '')
                    if entity_id not in seen_entities:
                        found_entities.append(Entity(
                            id=entity_id,
                            name=entity_data.get('name', ''),
                            type=entity_data.get('type', ''),
                            properties={k: v for k, v in entity_data.items() if k not in ['id', 'name', 'type']}
                        ))
                        seen_entities.add(entity_id)
                
                # Extract related entity and relationship
                if 'related' in record and record['related'] and 'r' in record and record['r']:
                    related_data = record['related']
                    rel_data = record['r']
                    
                    # Add related entity
                    related_id = related_data.get('id', '')
                    if related_id not in seen_entities:
                        found_entities.append(Entity(
                            id=related_id,
                            name=related_data.get('name', ''),
                            type=related_data.get('type', ''),
                            properties={k: v for k, v in related_data.items() if k not in ['id', 'name', 'type']}
                        ))
                        seen_entities.add(related_id)
                    
                    # Add relationship
                    found_relationships.append(Relationship(
                        source_id=entity_data.get('id', ''),
                        target_id=related_id,
                        relationship_type=rel_data.get('type', 'RELATES_TO'),
                        properties={k: v for k, v in rel_data.items() if k not in ['type']}
                    ))
            
            return GraphContext(
                entities=found_entities,
                relationships=found_relationships
            )
            
        except Exception as e:
            logger.error(f"Error in graph traversal: {e}")
            return None
    
    def _combine_context(self, semantic_results: List[Dict[str, Any]], graph_context: Optional[GraphContext]) -> str:
        """Combine semantic search results and graph context into a single context string"""
        context_parts = []
        
        # Add semantic search results
        if semantic_results:
            context_parts.append("## Relevant Documents:")
            for i, result in enumerate(semantic_results, 1):
                context_parts.append(f"{i}. {result['content']}")
                if result.get('metadata'):
                    context_parts.append(f"   Metadata: {result['metadata']}")
        
        # Add graph context
        if graph_context and graph_context.entities:
            context_parts.append("\n## Knowledge Graph Context:")
            
            # Add entities
            context_parts.append("### Entities:")
            for entity in graph_context.entities:
                context_parts.append(f"- {entity.name} ({entity.type})")
                if entity.properties:
                    props_str = ", ".join([f"{k}: {v}" for k, v in entity.properties.items()])
                    context_parts.append(f"  Properties: {props_str}")
            
            # Add relationships
            if graph_context.relationships:
                context_parts.append("\n### Relationships:")
                for rel in graph_context.relationships:
                    context_parts.append(f"- {rel.source_id} -[{rel.relationship_type}]-> {rel.target_id}")
                    if rel.properties:
                        props_str = ", ".join([f"{k}: {v}" for k, v in rel.properties.items()])
                        context_parts.append(f"  Properties: {props_str}")
        
        return "\n".join(context_parts)
    
    def _generate_answer(self, query: str, context: str) -> str:
        """Generate answer using OpenAI API"""
        try:
            prompt = f"""
You are a helpful AI assistant with access to both document content and knowledge graph relationships. 
Please answer the user's question based on the provided context.

User Question: {query}

Context:
{context}

Please provide a comprehensive answer that:
1. Directly addresses the user's question
2. Uses information from both the documents and knowledge graph relationships
3. Is accurate and well-structured
4. Acknowledges when information comes from the knowledge graph vs documents

Answer:
"""
            
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that combines document knowledge with graph relationships to provide accurate answers."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"I apologize, but I encountered an error while generating the answer: {str(e)}"
    
    def _calculate_confidence(self, semantic_results: List[Dict[str, Any]], graph_context: Optional[GraphContext]) -> float:
        """Calculate confidence score based on available information"""
        confidence = 0.0
        
        # Base confidence from semantic search
        if semantic_results:
            # Average distance (lower is better, so we invert)
            avg_distance = sum(r.get('distance', 1.0) for r in semantic_results) / len(semantic_results)
            confidence += (1.0 - avg_distance) * 0.6  # 60% weight for semantic search
        
        # Additional confidence from graph context
        if graph_context and graph_context.entities:
            confidence += 0.4  # 40% additional confidence for graph context
        
        return min(confidence, 1.0)  # Cap at 1.0
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Add a document to the system and extract entities for the graph"""
        try:
            # Generate document ID
            import uuid
            doc_id = str(uuid.uuid4())
            
            # Add to ChromaDB
            self.chroma_manager.add_documents(
                documents=[content],
                metadatas=[metadata or {}],
                ids=[doc_id]
            )
            
            # Extract entities and add to graph
            entities = self._extract_entities(content)
            for entity in entities:
                # Create entity in Neo4j
                entity_id = f"entity_{hash(entity) % 1000000}"
                self.neo4j_manager.create_entity(
                    entity_id=entity_id,
                    name=entity,
                    entity_type="GENERAL"  # Could be enhanced with entity classification
                )
            
            logger.info(f"Added document {doc_id} with {len(entities)} entities")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            raise 