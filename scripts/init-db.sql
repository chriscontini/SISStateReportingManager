-- Enable pgvector extension for vector embeddings (used in RAG/knowledge base)
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable UUID extension for future use
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
