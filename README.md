---
title: RAG Observability Platform
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 7860
---

# RAG Observability Platform 🚀

# RAG Observability Platform - Project Summary

## Project Overview

The **RAG Observability Platform** is a production-grade Retrieval-Augmented Generation (RAG) system that demonstrates advanced MLOps practices and hybrid cloud-local deployment strategies. It combines cutting-edge ML inference optimization (Apple Silicon GPU) with MLOps observability frameworks for enterprise-ready applications.

---

## What This Project Does

### Core Functionality
1. **Local RAG Pipeline (Mac M4)**
   - Ingests unstructured text documents
   - Chunks documents using recursive text splitting
   - Generates embeddings via sentence-transformers (optimized for Apple Silicon via MPS acceleration)
   - Stores embeddings in ChromaDB (local vector database)
   - Retrieves relevant context and generates answers using Llama 3.2 3B model via MLX

2. **Cloud Deployment (Hugging Face Spaces)**
   - Docker containerization for reproducible deployment
   - Automatic fallback to CPU-based inference when MLX unavailable
   - Streamlit web UI for interactive chat with documents
   - Graceful degradation: maintains functionality across platforms

3. **Experiment Tracking (Dagshub + MLflow)**
   - Logs all ingestion runs with parameters and metrics
   - Centralized experiment monitoring from local machine
   - Version control for code and data via Git + DVC
   - Remote MLflow server for team collaboration

### Technical Highlights
- **Cross-Platform Optimization**: Native M4 GPU (via MLX) for local development; CPU fallback for cloud
- **Infrastructure as Code**: Docker + UV for reproducible environments
- **Modern Python Stack**: LangChain (LCEL), Pydantic, asyncio-ready
- **MLOps Best Practices**: Experiment tracking, dependency management, secrets handling
---

## Key Highlight

1. **GPU Optimization**: Understand when to use specialized tools (MLX for Apple Silicon) vs. standard libraries (PyTorch)
2. **Cross-Platform Development**: Device abstraction, graceful fallbacks, testing on multiple architectures
3. **Dependency Management**: Using UV for faster resolution, managing optional dependencies (local vs. cloud groups)
4. **MLOps Practices**: Experiment tracking, versioning data + code, secrets management
5. **Production Deployment**: Docker best practices, environment variable injection, port mapping
6. **Modern Python**: Type hints, LangChain LCEL (functional composition), error handling
7. **Troubleshooting**: Resolved Python version mismatches, binary file handling in Git, device compatibility issues

---

## Why This Project Stands Out

- **Full Stack**: From local GPU optimization to cloud deployment
- **Senior-Level Considerations**: 
  - Device compatibility across platforms
  - Graceful degradation (MLX → Transformers fallback)
  - Secrets management without pushing `.env`
  - Experiment observability
- **Modern Tooling**: UV (faster than pip), MLX (Apple Silicon optimization), LangChain LCEL (declarative chains)
- **Problem Solving**: Resolved real-world issues (ONNX version compatibility, Docker base image mismatch, GPU device detection)

---

## GitHub/Portfolio Presentation

**Repository Structure** (visible in your GitHub):
```
rag-observability-platform/
├── src/
│   ├── ingestion/      (document loading, chunking, embedding)
│   ├── retrieval/      (RAG chain with LCEL)
│   └── generation/     (MLX wrapper, device handling)
├── app/frontend/       (Streamlit UI)
├── Dockerfile          (Cloud deployment)
├── pyproject.toml      (UV dependency management)
└── README.md           (project documentation)
```

**Git History** (visible in commits):
- Clean, semantic commits showing progression
- Branching strategy: `master` → `mvp` → `frontend`/`backend`
- Demonstrates collaborative workflow understanding

---

1. **"Why MLX instead of PyTorch?"**
   - MLX is optimized for Apple Silicon; PyTorch CPU mode is 10x slower on M4

2. **"How do you handle the MLX import error in Docker?"**
   - Try-except with fallback to transformers; dynamic device selection

3. **"Why use Dagshub for this portfolio project?"**
   - Demonstrates understanding of MLOps practices; shows ability to connect local experiments to remote tracking

4. **"What would you do at scale?"**
   - Move to managed inference (HF Inference API), DVC for larger datasets, Kubernetes for orchestration

---

