# Project: k8s_rag_agent_gemma

## Project Overview

This project is a template for creating and deploying a sophisticated AI agent. The agent is designed to use a Retrieval-Augmented Generation (RAG) architecture, which allows it to answer questions based on a private knowledge base. The intended technical stack includes:

*   **AI Model:** Google's Gemma
*   **Application Framework:** FastAPI (Python)
*   **Vector Database:** FAISS
*   **Embeddings Model:** `sentence-transformers/all-MiniLM-L6-v2`
*   **Containerization:** Docker
*   **Orchestration:** Kubernetes
*   **CI/CD:** GitHub Actions

The project is structured as a complete MLOps workflow, automating the process from code changes to deployment.

**Note:** This project is currently a template. The core application code, Dockerfile, and Kubernetes manifests are not yet implemented. The `README.md` file provides a detailed blueprint for the intended implementation.

## Knowledge Base

The AI agent's knowledge is based on the markdown files found in the `knowledge_base/` directory. The current knowledge base covers the following topics:

*   **DevFest Afrique Francophone:** Information about the annual developer event, its theme ("AI at the heart of Innovation"), objectives, and format.
*   **Google Developer Groups (GDG) in West Africa:** The mission of GDGs and a list of chapters in cities like Abidjan, Ouaga, Lomé, Cotonou, and Dakar.
*   **Consulting Services by Kimana MISAGO:** A description of the DevOps, Cloud Migration, AI, and Machine Learning services offered.

## Key Directories and Files

*   `README.md`: The main documentation for the project, outlining the architecture, setup, and deployment process.
*   `knowledge_base/`: Contains the markdown files that form the agent's private knowledge base.
*   `app/`: (Currently empty) Intended to hold the FastAPI application source code (`main.py`) and the vectorized knowledge base (`vector_db.faiss`).
*   `docker/`: (Currently empty) Intended to hold the `Dockerfile` for building the application container.
*   `kubernetes/`: (Currently empty) Intended to hold the Kubernetes manifests (`deployment.yaml`, `service.yaml`) for deploying the application.
*   `.github/workflows/`: (Currently empty) Intended to hold the GitHub Actions CI/CD pipeline definition (`cicd-pipeline.yml`).
*   `scripts/`: Contains helper scripts.
    *   `build_vector_db.py`: A script for converting the markdown files in `knowledge_base/` into a FAISS vector index. It uses the `sentence-transformers/all-MiniLM-L6-v2` model to generate embeddings.
    *   `requirements.txt`: Contains the Python dependencies for the `build_vector_db.py` script (`langchain`, `sentence-transformers`, `faiss-cpu`, `glob2`).

## Building and Running (Based on Project Plan)

The following commands are outlined in the `README.md` as the intended way to build and run the project.

**1. Create the Vector Database:**

The `scripts/build_vector_db.py` script reads all `.md` files in the `knowledge_base` directory, splits them into chunks, and then uses the `sentence-transformers/all-MiniLM-L6-v2` model to create embeddings. These embeddings are stored in a FAISS vector database, which is saved to `app/vector_db.faiss`.

```bash
# Install script dependencies
pip install -r scripts/requirements.txt

# Create the vector index from the knowledge base
python scripts/build_vector_db.py
```

**2. Build and Run with Docker (Local Testing):**

```bash
# Build the Docker image
docker build -t rag-agent:local .

# Run the container
docker run -p 8000:8000 rag-agent:local
```

**3. Deploy to Kubernetes:**

```bash
# Apply the Kubernetes manifests
kubectl apply -f kubernetes/
```

## Development Conventions

The project is designed around a CI/CD workflow. The `README.md` specifies that a GitHub Actions pipeline will be triggered on every push to the `main` branch. This pipeline will:

1.  Build the Docker image.
2.  Push the image to a container registry.
3.  Deploy the new image to the Kubernetes cluster.
