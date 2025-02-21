from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class Options(BaseModel):
    temperature: float = 0.7
    max_tokens: int = 123456

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: bool = False
    options: Optional[Options] = Options()

class KnowledgeRequest(BaseModel):
    similarity_threshold: float = 0.2
    vector_similarity_weight: float = 0.8
    use_kg: bool = False
    question: str
    doc_ids: List[str] = []
    kb_id: str
    page: int = 1
    size: int = 10

class ChatResponse(BaseModel):
    message: Message
    done: bool = True 