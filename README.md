# Graph RAG MVP

A complete Graph RAG (Retrieval-Augmented Generation) system that combines vector search with knowledge graphs for intelligent question answering.

## 🚀 What is Graph RAG?

Graph RAG enhances traditional RAG by adding a knowledge graph layer. Instead of just searching text chunks, it:

1. **Extracts entities** from queries and documents
2. **Builds relationships** between entities in a graph
3. **Combines semantic search** with **graph traversal**
4. **Generates more accurate** and **contextually rich** answers

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │   FastAPI       │    │   Databases     │
│   Frontend      │◄──►│   Backend       │◄──►│   ChromaDB      │
│                 │    │                 │    │   Neo4j         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Frontend (Next.js)
- Modern React interface with TypeScript
- Real-time query processing
- Document upload functionality
- Visual display of answers, sources, and graph context

### Backend (FastAPI)
- RESTful API with automatic documentation
- Graph RAG processing pipeline
- Entity extraction and graph building
- Integration with OpenAI for answer generation

### Databases
- **ChromaDB**: Vector database for semantic search
- **Neo4j**: Graph database for entity relationships

## 🛠️ Tech Stack

### Frontend
- **Next.js 15** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **React Hooks** for state management

### Backend
- **FastAPI** for high-performance API
- **Pydantic** for data validation
- **spaCy** for entity extraction
- **Sentence Transformers** for embeddings
- **OpenAI API** for LLM generation

### Databases
- **ChromaDB** for vector storage
- **Neo4j** for graph relationships

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 18+
- Neo4j (local or cloud)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd knowledge_graph_mvp
```

### 2. Backend Setup
```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Install spaCy model
python -m spacy download en_core_web_sm

# Copy environment template
cp env.example .env

# Edit .env with your settings
# Required: OPENAI_API_KEY, NEO4J_PASSWORD
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install Node.js dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### 4. Neo4j Setup

#### Option A: Local Neo4j
1. Download [Neo4j Desktop](https://neo4j.com/download/)
2. Create a new database
3. Set password in backend `.env`

#### Option B: Neo4j AuraDB (Cloud)
1. Sign up at [Neo4j AuraDB](https://neo4j.com/cloud/platform/aura-graph-database/)
2. Create a new database
3. Update connection details in backend `.env`

## 🚀 Running the Application

### 1. Start the Backend
```bash
cd backend
python -m app.main
```
API will be available at `http://localhost:8000`

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```
Frontend will be available at `http://localhost:3000`

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📖 Usage

### 1. Upload Documents
1. Go to the "Upload Document" section
2. Paste your document content
3. Click "Upload Document"
4. The system will extract entities and build relationships

### 2. Ask Questions
1. Type your question in the query box
2. Click "Ask Question"
3. View the answer with:
   - Confidence score
   - Processing time
   - Source documents
   - Knowledge graph context

### 3. Example Workflow
```
1. Upload: "John works at Microsoft in Seattle. Microsoft competes with Google."
2. Ask: "Where does John work?"
3. Answer: "John works at Microsoft in Seattle"
   - Sources: Document content
   - Graph: John → works_at → Microsoft
```

## 🔧 API Endpoints

### Query Processing
- `POST /api/query/` - Process Graph RAG queries
- `GET /api/query/health` - Query service health

### Document Management
- `POST /api/documents/upload` - Upload single document
- `POST /api/documents/batch-upload` - Upload multiple documents
- `GET /api/documents/stats` - Get document statistics

### System Health
- `GET /health` - Overall system health
- `GET /docs` - Interactive API documentation

## 🏗️ Project Structure

```
knowledge_graph_mvp/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   └── types/           # TypeScript types
│   └── package.json
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── models/          # Pydantic schemas
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utilities
│   ├── data/                # Database files
│   │   ├── chroma/          # ChromaDB data
│   │   └── neo4j/           # Neo4j data
│   └── requirements.txt
└── README.md
```

## 🔍 How Graph RAG Works

### 1. Document Processing
```
Document → Entity Extraction → Graph Building
         ↓
    Vector Embedding → ChromaDB Storage
```

### 2. Query Processing
```
Query → Entity Extraction → Parallel Retrieval
      ↓                    ↓
   Vector Search        Graph Traversal
   (ChromaDB)          (Neo4j)
      ↓                    ↓
   Text Context        Graph Context
      ↓                    ↓
      Combined Context → LLM → Answer
```

### 3. Benefits
- **Better Context**: Understands relationships between entities
- **Reduced Hallucinations**: Grounded in structured knowledge
- **Deeper Insights**: Can discover connections across documents

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Backend Deployment
```bash
# Using uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Using Docker (when implemented)
docker build -t graph-rag-backend .
docker run -p 8000:8000 graph-rag-backend
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Deploy to Vercel
vercel --prod
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
# Required
OPENAI_API_KEY=your_openai_api_key
NEO4J_PASSWORD=your_neo4j_password

# Optional
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

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

4. **Frontend Can't Connect to Backend**
   - Verify backend is running on port 8000
   - Check CORS settings
   - Ensure `NEXT_PUBLIC_API_URL` is correct

### Logs
- Backend logs to stdout
- Check for database connection messages
- Look for query processing logs

## 🚀 Next Steps

### Immediate Improvements
- [ ] Add authentication
- [ ] Implement document chunking
- [ ] Add relationship extraction
- [ ] Implement caching
- [ ] Add monitoring and metrics

### Advanced Features
- [ ] Multi-modal support (images, PDFs)
- [ ] Real-time collaboration
- [ ] Advanced graph visualization
- [ ] Custom embedding models
- [ ] A/B testing framework

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For questions and support:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation at `/docs`

---

**Built with ❤️ for intelligent question answering** 