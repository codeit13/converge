"""
faiss_rag_service.py
--------------------
A service for Retrieval-Augmented Generation (RAG) using FAISS and LangChain.
This service provides functions to create a FAISS vector store from documents (e.g., chat history),
perform similarity search, and answer questions using a retriever and LLM.

References:
- LangChain QA Chat History Tutorial: https://python.langchain.com/docs/tutorials/qa_chat_history/
"""

from typing import List, Optional, Callable, Dict, Any, Union
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, UnstructuredPDFLoader, WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
import os
import mimetypes
import requests

from config import settings


class FAISSRAGService:
    """
    Retrieval-Augmented Generation (RAG) service with FAISS and LangChain.
    Supports multi-source data ingestion (str, txt, pdf, url, etc.), chunking, deduplication, persistence, and extensibility.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        self.embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        self.vector_store: Optional[FAISS] = None
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Loader registry: extension or type -> loader function
        self.loader_registry: Dict[str, Callable[[
            Any], List[Document]]] = self._default_loader_registry()

    def _default_loader_registry(self) -> Dict[str, Callable[[Any], List[Document]]]:
        return {
            "txt": self._load_txt,
            "pdf": self._load_pdf,
            "md": self._load_txt,
            "url": self._load_url,
            "str": self._load_str
        }

    def register_loader(self, key: str, loader_func: Callable[[Any], List[Document]]):
        """Register a custom loader for a file extension or type."""
        self.loader_registry[key] = loader_func

    def load_data(self, sources: List[Union[str, Path]], metadatas: Optional[List[dict]] = None, deduplicate: bool = True) -> List[Document]:
        """
        Load and chunk data from multiple sources (str, file, url, etc.). Returns list of Documents.
        Each Document will be assigned a unique doc_id (hash of content).
        """
        import hashlib
        docs = []
        for i, src in enumerate(sources):
            doc_meta = metadatas[i] if metadatas and i < len(metadatas) else {}
            if isinstance(src, str) and src.startswith("http"):
                loader = self.loader_registry.get("url", self._load_url)
                loaded = loader(src)
            elif isinstance(src, str) and os.path.isfile(src):
                ext = os.path.splitext(src)[-1][1:].lower()
                loader = self.loader_registry.get(ext, self._load_txt)
                loaded = loader(src)
            elif isinstance(src, Path) and src.exists():
                ext = src.suffix[1:].lower()
                loader = self.loader_registry.get(ext, self._load_txt)
                loaded = loader(str(src))
            elif isinstance(src, str):
                loader = self.loader_registry.get("str", self._load_str)
                loaded = loader(src)
            else:
                continue
            # Attach metadata and doc_id
            for doc in loaded:
                content_hash = hashlib.sha256(
                    doc.page_content.encode("utf-8")).hexdigest()
                doc.metadata["doc_id"] = content_hash
                doc.metadata.update(doc_meta)
            docs.extend(loaded)
        # Deduplicate by content
        if deduplicate:
            seen = set()
            unique_docs = []
            for doc in docs:
                if doc.page_content not in seen:
                    seen.add(doc.page_content)
                    unique_docs.append(doc)
            docs = unique_docs
        return docs

    def _load_txt(self, path: str) -> List[Document]:
        loader = TextLoader(path)
        docs = loader.load()
        return self._split_docs(docs)

    def _load_pdf(self, path: str) -> List[Document]:
        loader = UnstructuredPDFLoader(path)
        docs = loader.load()
        return self._split_docs(docs)

    def _load_url(self, url: str) -> List[Document]:
        loader = WebBaseLoader(url)
        docs = loader.load()
        return self._split_docs(docs)

    def _load_str(self, text: str) -> List[Document]:
        return self._split_docs([Document(page_content=text)])

    def _split_docs(self, docs: List[Document]) -> List[Document]:
        splitter = CharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        return splitter.split_documents(docs)

    def build_vector_store(self, docs: List[Document]):
        self.vector_store = FAISS.from_documents(docs, self.embeddings)
        self.documents = docs  # Track all docs in memory

    def add_documents(self, docs: List[Document]):
        if not hasattr(self, 'documents') or self.documents is None:
            self.documents = []
        self.documents.extend(docs)
        if not self.vector_store:
            self.build_vector_store(self.documents)
        else:
            self.vector_store.add_documents(docs)

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        if not self.vector_store:
            raise ValueError(
                "Vector store not initialized. Call build_vector_store or add_documents first.")
        return self.vector_store.similarity_search(query, k=k)

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by its doc_id and rebuild the vector store."""
        if not hasattr(self, 'documents') or self.documents is None:
            return False
        new_docs = [doc for doc in self.documents if doc.metadata.get(
            'doc_id') != doc_id]
        if len(new_docs) == len(self.documents):
            return False  # No doc deleted
        self.documents = new_docs
        if self.documents:
            self.build_vector_store(self.documents)
        else:
            self.vector_store = None
        return True

    def get_retriever(self):
        if not self.vector_store:
            raise ValueError("Vector store not initialized.")
        return self.vector_store.as_retriever()

    def get_qa_chain(self, llm: BaseLanguageModel, chain_type: str = "stuff"):
        retriever = self.get_retriever()
        return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type=chain_type)

    def save_index(self, path: str):
        if self.vector_store:
            self.vector_store.save_local(path)

    def load_index(self, path: str):
        self.vector_store = FAISS.load_local(path, self.embeddings)

# Example usage:
# rag = FAISSRAGService()
# docs = rag.load_data(["Hello world", "myfile.txt", "https://example.com", "myfile.pdf"])
# rag.build_vector_store(docs)
# rag.save_index("faiss.idx")
# rag.load_index("faiss.idx")
# results = rag.similarity_search("What is LangChain?")
# retriever = rag.get_retriever()
# qa_chain = rag.get_qa_chain(llm)
