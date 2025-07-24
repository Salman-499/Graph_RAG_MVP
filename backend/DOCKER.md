# Docker Setup for Graph RAG Backend

This guide explains how to run the Graph RAG backend using Docker while keeping the frontend running with npm commands.

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key
- Node.js and npm (for frontend)

## Quick Start

1. **Set up environment variables:**
   ```bash
   cd backend
   cp env.docker.example .env
   # Edit .env and add your OpenAI API key
   ```

2. **Start the backend services:**
   ```bash
   docker-compose up -d
   ```

3. **Start the frontend (in a separate terminal):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the applications:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Neo4j Browser: http://localhost:7474 (neo4j/password123)

## Architecture

The Docker setup includes:

- **FastAPI Backend** (Port 8000): Main application server
- **Neo4j Database** (Ports 7474, 7687): Graph database for knowledge graphs
- **ChromaDB**: Vector database (file-based, persisted in volumes)

## Environment Variables

All services use a single `.env` file for configuration. Key variables:

### Backend API Configuration
```env
OPENAI_API_KEY=your_openai_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

### Neo4j Database Configuration
```env
# Connection settings (for backend to connect)
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123

# Container settings (for Neo4j service)
NEO4J_AUTH=neo4j/password123
NEO4J_PLUGINS=["apoc"]
```

### ChromaDB Configuration
```env
CHROMA_PERSIST_DIRECTORY=/app/data/chroma
```

The complete environment file structure is organized into sections for easy management.

## Docker Commands

### Start Services
```bash
# Start all services in background
docker-compose up -d

# Start with logs visible
docker-compose up

# Start specific service
docker-compose up backend
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes data)
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f neo4j
```

### Rebuild Services
```bash
# Rebuild after code changes
docker-compose build backend

# Rebuild and restart
docker-compose up --build -d
```

## Development Workflow

### Making Code Changes

The backend container uses volume mounting, so code changes are reflected immediately:

1. Edit Python files in `app/`
2. The FastAPI server will auto-reload
3. No need to rebuild the container

### Database Management

**Neo4j:**
- Access Neo4j Browser at http://localhost:7474
- Username: `neo4j`, Password: `password123`
- Data persists in Docker volumes

**ChromaDB:**
- File-based database in `data/chroma/`
- Data persists between container restarts

### Debugging

**View backend logs:**
```bash
docker-compose logs -f backend
```

**Execute commands in backend container:**
```bash
docker-compose exec backend bash
```

**Check service health:**
```bash
curl http://localhost:8000/health
```

## Production Considerations

For production deployment:

1. **Update environment variables:**
   - Use strong passwords
   - Set `DEBUG=false`
   - Configure proper Neo4j memory settings

2. **Use production Dockerfile:**
   ```dockerfile
   # Remove --reload flag
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. **Add reverse proxy:**
   - Use nginx or similar
   - Configure SSL/TLS
   - Set up proper domain names

4. **Backup strategy:**
   - Regular Neo4j database backups
   - ChromaDB data backup
   - Environment configuration backup

## Troubleshooting

### Common Issues

**Port conflicts:**
```bash
# Check what's using port 8000
lsof -i :8000
# Kill process if needed
kill -9 <PID>
```

**Neo4j connection issues:**
```bash
# Check Neo4j logs
docker-compose logs neo4j

# Restart Neo4j
docker-compose restart neo4j
```

**Backend won't start:**
```bash
# Check backend logs
docker-compose logs backend

# Rebuild container
docker-compose build --no-cache backend
```

### Reset Everything

To start fresh:
```bash
# Stop and remove everything
docker-compose down -v

# Remove images
docker-compose build --no-cache

# Start fresh
docker-compose up -d
```

## File Structure

```
backend/
├── Dockerfile              # Backend container definition
├── docker-compose.yml      # Service orchestration
├── .dockerignore           # Files to exclude from build
├── env.docker.example      # Environment template
├── app/                    # FastAPI application
├── data/                   # Persistent data (mounted)
│   ├── chroma/            # ChromaDB files
│   └── neo4j/             # Neo4j data (if needed)
└── requirements.txt        # Python dependencies
```

## Monitoring

**Health checks:**
- Backend: http://localhost:8000/health
- Neo4j: http://localhost:7474

**Resource usage:**
```bash
docker stats
```

This setup provides a robust, scalable backend infrastructure while keeping the frontend development workflow simple with npm commands. 