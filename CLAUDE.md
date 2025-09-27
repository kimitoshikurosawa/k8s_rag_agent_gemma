# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a MLOps project for deploying a RAG (Retrieval-Augmented Generation) AI agent using Gemma model and Kubernetes. The project demonstrates a complete MLOps workflow from code modification to production deployment.

## Architecture

The project follows a RAG architecture:
1. **Retrieval**: Agent searches relevant information from a private knowledge base (Markdown files)
2. **Augmentation**: Injects retrieved information into Gemma model prompts
3. **Generation**: Gemma generates precise, factual responses using the context

The MLOps pipeline automates: code changes → Docker build → container registry push → Kubernetes deployment.

## Key Development Commands

### Building the Vector Database
```bash
# Install script dependencies
pip install -r scripts/requirements.txt

# Create vector database from knowledge base
python scripts/build_vector_db.py
```
This generates `app/vector_db.faiss` from markdown files in `knowledge_base/`.

### Local Development with Docker
```bash
# Build the application image
docker build -t rag-agent:local .

# Run locally on port 8000
docker run -p 8000:8000 rag-agent:local

# Test the agent
curl -X POST "http://localhost:8000/generate" \
-H "Content-Type: application/json" \
-d '{"prompt": "Your question here"}'
```

### Kubernetes Deployment
```bash
# Deploy to cluster
kubectl apply -f kubernetes/

# Check deployment status
kubectl get pods

# Port forward for testing
kubectl port-forward service/rag-agent-service 8080:80

# Test on cluster
curl -X POST "http://localhost:8080/generate" \
-H "Content-Type: application/json" \
-d '{"prompt": "Your question here"}'
```

## Project Structure

- `app/`: FastAPI application with RAG logic and generated vector database
- `knowledge_base/`: Markdown files containing agent's knowledge sources
- `scripts/`: Vector database creation utilities
- `docker/`: Dockerfile for containerization
- `kubernetes/`: K8s deployment and service manifests
- `.github/workflows/`: CI/CD pipeline (when created)

## Development Workflow

1. **Update Knowledge**: Modify/add markdown files in `knowledge_base/`
2. **Rebuild Vector DB**: Run `python scripts/build_vector_db.py`
3. **Test Locally**: Build and run Docker container
4. **Deploy**: Push changes to trigger CI/CD or manually apply K8s manifests

## Important Notes

- The vector database must be regenerated after any changes to the knowledge base
- All Python dependencies are managed via requirements.txt files in respective directories
- The project is designed for conference demonstrations showing real-time knowledge updates