# Graph RAG MVP

A question-answering app that combines vector search with a knowledge graph. Plain RAG only retrieves text chunks similar to the question. Here, the entities in a question also pull in related facts from a graph, so answers can use connections between documents.

## How it works

**Adding a document**
1. The text is embedded with a Sentence-Transformers model (`all-MiniLM-L6-v2` by default) and stored in ChromaDB.
2. spaCy extracts named entities, which are stored as nodes in Neo4j.

**Asking a question**
1. spaCy extracts the entities in the question.
2. ChromaDB returns the most similar chunks.
3. Neo4j returns the matching entities and their relationships.
4. Both are combined into one context, and an OpenAI model (`gpt-3.5-turbo` by default) writes the answer.

## Stack

- **Backend:** FastAPI, ChromaDB, Neo4j 5, Sentence-Transformers, spaCy, OpenAI API
- **Frontend:** Next.js and TypeScript
- **Deployment:** Docker Compose; `ec2-setup.sh` sets up the backend on an AWS EC2 instance

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/documents/upload` | Add one document |
| POST | `/api/documents/batch-upload` | Add several documents |
| GET | `/api/documents/stats` | Document and entity counts |
| POST | `/api/query/` | Ask a question |
| GET | `/api/query/health` | Health check |

## Running it

```bash
cd backend
cp env.example .env          # add OPENAI_API_KEY and the Neo4j password
docker-compose up --build    # API on :8000, Neo4j browser on :7474

cd ../frontend
cp env.example .env.local
npm install && npm run dev
```
