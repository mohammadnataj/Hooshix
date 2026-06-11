from typing import List, Dict, Any
import time


class MemoryItem:
    def __init__(self, content: str, metadata: Dict[str, Any] = None):
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


class MemoryStore:
    """
    Simple in-memory storage for Hooshix Agent.
    Phase 1: no vector DB, no embeddings, just structured memory.
    """

    def __init__(self):
        self.memories: List[MemoryItem] = []

    def add_memory(self, content: str, metadata: Dict[str, Any] = None):
        memory = MemoryItem(content, metadata)
        self.memories.append(memory)
        return memory

    def get_all_memories(self) -> List[Dict]:
        return [m.to_dict() for m in self.memories]

    def search_memory(self, keyword: str) -> List[Dict]:
        """
        Very simple keyword search (Phase 1 approach)
        """
        results = []
        for m in self.memories:
            if keyword.lower() in m.content.lower():
                results.append(m.to_dict())
        return results

    def clear(self):
        self.memories = []
