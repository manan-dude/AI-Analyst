# app/api/routes/rag.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.models.request_models import RAGQueryRequest
from app.services.rag_service import rag_service
from app.config import settings
from app.utils.logger import logger

router = APIRouter(prefix="/api/rag", tags=["RAG Analyzer"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload document for RAG."""
    logger.info("="*70)
    logger.info("📄 RAG DOCUMENT UPLOAD")
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files supported")
    
    try:
        # Save file
        file_path = settings.UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Extract text
        text = await rag_service.extract_text_from_pdf(
            str(file_path),
            max_pages=settings.MAX_PAGES_RAG
        )
        
        # Chunk text
        chunks = rag_service.chunk_text(text)
        
        # Create collection
        collection_name = f"user_documents_{file.filename.replace('.pdf', '')}"
        collection = rag_service.create_collection(collection_name)
        
        # Add documents
        rag_service.add_documents_to_collection(collection, chunks)
        
        logger.info("✅ Document uploaded and processed")
        return JSONResponse(content={
            "success": True,
            "collection_name": collection_name,
            "chunks_created": len(chunks)
        })
        
    except Exception as e:
        logger.error(f"❌ Document upload failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@router.post("/query")
async def query_documents(request: RAGQueryRequest):
    """Query RAG documents."""
    logger.info("="*70)
    logger.info(f"🔍 RAG QUERY: {request.query}")
    
    try:
        # Query collection
        context_chunks = rag_service.query_collection(
            request.collection_name,
            request.query
        )
        
        # Generate response
        answer = rag_service.generate_rag_response(request.query, context_chunks)
        
        logger.info("✅ RAG query completed")
        return JSONResponse(content={
            "success": True,
            "answer": answer
        })
        
    except Exception as e:
        logger.error(f"❌ RAG query failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
