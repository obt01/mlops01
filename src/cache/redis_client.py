from __future__ import annotations
import json
import redis
from pydantic import BaseModel
from typing import Optional, Any


r = redis.Redis(
    host="redis",
    port=6379,
)

def set_data_redis(key: str, value: dict) -> bool:
    data_json = json.dumps(value)
    r.set(key, data_json)
    return True


def get_data_redis(key: str) -> Optional[list]:
    data = r.get(key)
    if data is None:
        return None
    else:
        return json.loads(data)


class SaveDataRedisJob(BaseModel):
    key: str
    value: dict
    is_completed: bool = False

    def __call__(self):
        self.is_completed = set_data_redis(key=self.key, value=self.value)


def save_data_job(key: str, value: dict) -> str:
    task = SaveDataRedisJob(key=key, value=value)
    task()
    return key
