from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
from services.rag_service import FAISSRAGService

router = APIRouter()

# Singleton RAG service instance (reuse or replace as needed)
rag_service = FAISSRAGService()

class DocumentPreview(BaseModel):
    doc_id: str
    content_preview: str
    metadata: dict

class AddDocumentResponse(BaseModel):
    status: str
    added_docs: int

class GetKnowledgeBaseResponse(BaseModel):
    documents: List[DocumentPreview]

class SearchRequest(BaseModel):
    query: str
    k: Optional[int] = 5

class SearchResponse(BaseModel):
    results: List[DocumentPreview]

@router.post("/documents", response_model=AddDocumentResponse)
async def add_document(
    source_type: str = Form(..., description="text, file, or url"),
    content: Optional[str] = Form(None, description="Text content or URL. Required for text/url."),
    file: Optional[UploadFile] = File(None, description="File to upload. Required for file type."),
    metadata: Optional[str] = Form(None, description="Optional metadata as JSON string")
):
    import json
    metadict = json.loads(metadata) if metadata else {}
    docs = []
    if source_type == "text":
        if not content:
            raise HTTPException(status_code=400, detail="Text content required.")
        docs = rag_service.load_data([content], metadatas=[metadict])
    elif source_type == "url":
        if not content:
            raise HTTPException(status_code=400, detail="URL required.")
        docs = rag_service.load_data([content], metadatas=[metadict])
    elif source_type == "file":
        if not file:
            raise HTTPException(status_code=400, detail="File required.")
        import tempfile
        suffix = "." + file.filename.split(".")[-1] if "." in file.filename else ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        docs = rag_service.load_data([tmp_path], metadatas=[metadict])
        import os
        os.unlink(tmp_path)
    else:
        raise HTTPException(status_code=400, detail="Invalid source_type. Use 'text', 'file', or 'url'.")
    rag_service.add_documents(docs)
    return AddDocumentResponse(status="success", added_docs=len(docs))

@router.get("/documents", response_model=GetKnowledgeBaseResponse)
async def get_knowledge_base():
    docs = getattr(rag_service, "documents", None)
    if not docs:
        return GetKnowledgeBaseResponse(documents=[])
    previews = [
        DocumentPreview(
            doc_id=doc.metadata.get("doc_id", ""),
            content_preview=doc.page_content[:200],
            metadata={k: v for k, v in doc.metadata.items() if k != "doc_id"}
        )
        for doc in docs
    ]
    return GetKnowledgeBaseResponse(documents=previews)

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    deleted = rag_service.delete_document(doc_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "success", "doc_id": doc_id}

@router.post("/search", response_model=SearchResponse)
async def search_knowledge_base(request: SearchRequest):
    if not rag_service.vector_store:
        return SearchResponse(results=[])
    docs = rag_service.similarity_search(request.query, k=request.k or 5)
    results = [
        DocumentPreview(
            doc_id=doc.metadata.get("doc_id", ""),
            content_preview=doc.page_content[:200],
            metadata={k: v for k, v in doc.metadata.items() if k != "doc_id"}
        )
        for doc in docs
    ]
    return SearchResponse(results=results)
