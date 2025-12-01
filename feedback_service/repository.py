import json
import os
import threading
from typing import List, Dict

class FeedbackRepository:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self._lock = threading.Lock()
        self._ensure_storage()

    def _ensure_storage(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_feedback(self, record: Dict) -> Dict:
        with self._lock:
            records = self._read_all()
            records.append(record)
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
        return record

    def list_feedback(self) -> List[Dict]:
        with self._lock:
            return self._read_all()

    def _read_all(self) -> List[Dict]:
        if not os.path.exists(self.storage_path):
            return []
        with open(self.storage_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

