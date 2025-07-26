#!/bin/bash

# EC2 Setup Script for Graph RAG MVP Backend
set -e

echo "🚀 Setting up Graph RAG MVP Backend on EC2..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

print_status "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

print_status "Installing Docker..."
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

print_status "Installing Docker Compose..."
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

print_status "Installing Node.js for frontend..."
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

print_status "Creating application directory..."
# Create app directory
mkdir -p ~/graph-rag-mvp
cd ~/graph-rag-mvp

print_status "Setting up firewall..."
# Configure firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 8000
sudo ufw allow 7474
sudo ufw --force enable

print_status "Creating environment file..."
# Create .env file
cat > backend/.env << EOF
# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY=/app/data/chroma
CHROMA_COLLECTION_NAME=documents

# Backend connection settings (for Python code to connect to Neo4j)
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123

# Embedding Settings
EMBEDDING_MODEL=paraphrase-MiniLM-L3-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Processing Settings
MAX_TOKENS=4000
TEMPERATURE=0.7

# Logging level
LOG_LEVEL=INFO
EOF

print_warning "Please edit backend/.env and add your OpenAI API key before continuing."
print_warning "Press Enter when ready to continue..."
read

print_status "Starting services..."
cd backend
docker-compose up -d

print_status "Waiting for services to be ready..."
sleep 30

print_status "Checking service health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status "✅ Backend is healthy"
else
    print_error "❌ Backend health check failed"
    docker-compose logs backend
    exit 1
fi

print_status "🎉 Setup completed successfully!"

echo ""
echo "📋 Service URLs:"
echo "   Backend API: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'localhost'):8000"
echo "   API Documentation: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'localhost'):8000/docs"
echo "   Neo4j Browser: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'localhost'):7474"
echo ""
echo "🔧 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   Update services: docker-compose pull && docker-compose up -d"
echo ""
echo "📝 Next steps:"
echo "   1. Update your frontend to point to the EC2 backend URL"
echo "   2. Configure your domain (optional)"
echo "   3. Set up SSL/TLS (recommended for production)"
echo "" 