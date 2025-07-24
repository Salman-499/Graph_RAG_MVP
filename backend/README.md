# Graph RAG MVP Backend

A FastAPI-based backend for a Graph RAG (Retrieval-Augmented Generation) system that combines vector search with knowledge graphs.

## Architecture

This backend implements the Graph RAG pattern with the following components:

- **FastAPI**: Web framework for the API
- **ChromaDB**: Vector database for semantic search
- **Neo4j**: Graph database for knowledge graph relationships
- **OpenAI**: LLM for answer generation
- **spaCy**: Entity extraction from text
- **Sentence Transformers**: Text embeddings

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 3. Set up Neo4j

You have several options:

#### Option A: Local Neo4j (Recommended for MVP)
1. Download Neo4j Desktop or Neo4j Community Edition
2. Create a new database
3. Set the password in your `.env` file

#### Option B: Neo4j AuraDB (Cloud)
1. Sign up at https://neo4j.com/cloud/platform/aura-graph-database/
2. Create a new database
3. Update the connection details in your `.env` file

### 4. Environment Configuration

Copy `env.example` to `.env` and configure:

```bash
cp env.example .env
```

Required settings:
- `OPENAI_API_KEY`: Your OpenAI API key
- `NEO4J_PASSWORD`: Your Neo4j password

## Running the Application

### Development Mode

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
- `GET /health` - Check system health and database status

### Query Processing
- `POST /api/query/` - Process a Graph RAG query
- `GET /api/query/health` - Query service health check

### Document Management
- `POST /api/documents/upload` - Upload a single document
- `POST /api/documents/batch-upload` - Upload multiple documents
- `GET /api/documents/stats` - Get document statistics

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## How Graph RAG Works

1. **Query Processing**: User query is received
2. **Entity Extraction**: Named entities are extracted using spaCy
3. **Parallel Retrieval**:
   - Semantic search in ChromaDB using embeddings
   - Graph traversal in Neo4j starting from extracted entities
4. **Context Assembly**: Results from both sources are combined
5. **Answer Generation**: OpenAI LLM generates the final answer

## Directory Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── routers/
│   │   ├── query.py         # Query endpoints
│   │   └── documents.py     # Document management
│   ├── services/
│   │   └── graph_rag_service.py  # Core Graph RAG logic
│   └── utils/
│       ├── config.py        # Configuration management
│       └── database.py      # Database connections
├── data/
│   ├── chroma/              # ChromaDB data
│   └── neo4j/               # Neo4j data (if local)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Development

### Adding New Features

1. **New Endpoints**: Add to appropriate router in `app/routers/`
2. **New Models**: Add to `app/models/schemas.py`
3. **New Services**: Add to `app/services/`
4. **Database Changes**: Update `app/utils/database.py`

### Testing

```bash
# Run tests (when implemented)
pytest

# Check code formatting
black app/
isort app/
```

## Troubleshooting

### Common Issues

1. **Neo4j Connection Failed**
   - Check if Neo4j is running
   - Verify connection details in `.env`
   - Ensure firewall allows connection

2. **OpenAI API Errors**
   - Verify API key is correct
   - Check API quota and billing

3. **ChromaDB Issues**
   - Ensure data directory is writable
   - Check disk space

### Logs

The application logs to stdout. Check for:
- Database connection messages
- Query processing logs
- Error messages

## Next Steps

- Add authentication
- Implement document chunking
- Add relationship extraction
- Implement caching
- Add monitoring and metrics 