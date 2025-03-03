import json
import os
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any

from app.core.config import settings

# Simple file-based storage for composition metadata
class CompositionStorage:
    _instance = None
    _compositions = {}
    _lock = threading.Lock()
    
    def __new__(cls, metadata_file=None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CompositionStorage, cls).__new__(cls)
                cls._instance._metadata_file = metadata_file or os.path.join(settings.MIDI_FILES_DIR, "metadata.json")
                cls._instance._instance_lock = threading.Lock()
                cls._instance._load_metadata()
            return cls._instance
    
    def _load_metadata(self):
        """Load composition metadata from file"""
        if os.path.exists(self._metadata_file):
            try:
                with open(self._metadata_file, "r") as f:
                    self._compositions = json.load(f)
            except json.JSONDecodeError:
                self._compositions = {}
    
    def _save_metadata(self):
        """Save composition metadata to file"""
        with open(self._metadata_file, "w") as f:
            json.dump(self._compositions, f, indent=2)
    
    def add_composition(self, composition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new composition to storage"""
        with self._instance_lock:
            composition_id = composition_data["id"]
            self._compositions[composition_id] = composition_data
            self._save_metadata()
            return composition_data
    
    def get_composition(self, composition_id: str) -> Optional[Dict[str, Any]]:
        """Get a composition by ID"""
        return self._compositions.get(composition_id)
    
    def list_compositions(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List compositions with pagination"""
        compositions_list = list(self._compositions.values())
        total = len(compositions_list)
        
        # Sort by creation time (newest first)
        compositions_list.sort(key=lambda c: c["created_at"], reverse=True)
        
        # Apply pagination
        paginated_compositions = compositions_list[skip:skip + limit]
        
        return {
            "compositions": paginated_compositions,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "size": limit
        }