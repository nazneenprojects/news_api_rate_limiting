import json
from typing import Optional, Dict, Any, List
import asyncio
from pathlib import Path

class DataModel:
    def __init__(self, data_file:str = "/home/zermatt/Downloads/PythonBackendEng/asyncio_project_jsondata/sample_data.json"):
        self.data_file = data_file
        self.data: Dict[str, List[Dict[str, Any]]] = {}
        self._loaded = False
        self._lock = asyncio.Lock()


    async def load_data(self) -> None:
        async with self._lock:
            if not self._loaded:
                try:
                    data_path = Path(self.data_file)
                    with open(data_path, "r") as f:
                        self.data = json.load(f)
                    self._loaded = True
                except Exception as e:
                    raise RuntimeError("failed to load data", e)

    async def ensure_data_loaded(self) -> None:
        if not self._loaded:
            await self.load_data()

    async def get_users(self) -> List[Dict[str, Any]]:
        """
        Get users with pagination.
        """
        await self.ensure_data_loaded()
        return self.data.get("users", [])

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a single user by ID.
        """
        await self.ensure_data_loaded()
        users = self.data.get("users", [])
        for user in users:
            if user["id"] == user_id:
                return user
        return None
