# app/services/rag_service.py
import fitz
import asyncio
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.clients import gemini_client, chroma_client
from app.config import settings
from app.utils.logger import logger

class RAGService:
    """Service for RAG operations."""
    
    @staticmethod
    async def extract_text_from_pdf(pdf_path: str, max_pages: int = None) -> str:
        """Extract text from PDF file."""
        logger.info(f"📄 Extracting text from PDF: {pdf_path}")
        
        def extract():
            doc = fitz.open(pdf_path)
            pages_to_process = min(max_pages or len(doc), len(doc))
            text = ""
            for page_num in range(pages_to_process):
                text += doc[page_num].get_text()
            doc.close()
            return text
        
        text = await asyncio.to_thread(extract)
        logger.info(f"✅ Extracted {len(text)} characters from {pdf_path}")
        return text
    
    @staticmethod
    def chunk_text(text: str) -> List[str]:
        """Split text into chunks."""
        logger.info(f"✂️ Chunking text: {len(text)} characters")
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len
        )
        chunks = splitter.split_text(text)
        logger.info(f"✅ Created {len(chunks)} chunks")
        return chunks
    
    @staticmethod
    def create_collection(collection_name: str):
        """Create or get ChromaDB collection."""
        logger.info(f"📦 Creating collection: {collection_name}")
        
        try:
            chroma_client.delete_collection(name=collection_name)
        except:
            pass
        
        collection = chroma_client.create_collection(name=collection_name)
        logger.info(f"✅ Collection created: {collection_name}")
        return collection
    
    @staticmethod
    def add_documents_to_collection(collection, chunks: List[str]):
        """Add document chunks to ChromaDB."""
        logger.info(f"💾 Adding {len(chunks)} documents to collection")
        
        # Generate embeddings
        embeddings = []
        for i in range(0, len(chunks), 10):
            batch = chunks[i:i+10]
            response = gemini_client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=batch
            )
            embeddings.extend([item.values for item in response.embeddings])
        
        # Add to collection
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[f"chunk_{i}" for i in range(len(chunks))]
        )
        logger.info(f"✅ Added {len(chunks)} documents to collection")
    
    @staticmethod
    def query_collection(collection_name: str, query: str, n_results: int = 3) -> List[str]:
        """Query ChromaDB collection."""
        logger.info(f"🔍 Querying collection: {collection_name}")
        
        collection = chroma_client.get_collection(name=collection_name)
        
        # Generate query embedding
        response = gemini_client.models.embed_content(
            model=settings.EMBEDDING_MODEL,
            contents=[query]
        )
        query_embedding = response.embeddings.values
        
        # Query collection
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        logger.info(f"✅ Found {len(results['documents'])} relevant chunks")
        return results['documents']
    
    @staticmethod
    def generate_rag_response(query: str, context_chunks: List[str]) -> str:
        """Generate response using RAG."""
        logger.info("🤖 Generating RAG response...")
        
        context = "\n\n".join(context_chunks)
        
        prompt = f"""
You are a helpful AI assistant. Answer the user's question based on the provided context.

CONTEXT:
{context}

QUESTION:
{query}

Provide a clear, accurate answer based on the context. If the context doesn't contain enough information, say so.
"""
        
        response = gemini_client.models.generate_content(
            model=settings.GENERATIVE_MODEL,
            contents=prompt
        )
        
        return response.text

rag_service = RAGService()
