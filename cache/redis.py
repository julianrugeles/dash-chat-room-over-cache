import redis
import json
from typing import List, Dict
import datetime

class RedisManager:
    def __init__(self, host="localhost", port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def save_message(self, room_id: str, user: str, text: str) -> None:

        msg = {
            "user": user,
            "text": text,
            "time": datetime.datetime.now().strftime("%H:%M:%S")
        }
        self.r.rpush(f"room:{room_id}", json.dumps(msg))

    def get_messages(self, room_id: str, limit: int = 50) -> List[Dict]:
        msgs = self.r.lrange(f"room:{room_id}", -limit, -1)
        return [json.loads(m) for m in msgs]

    def clear_room(self, room_id: str) -> None:
        self.r.delete(f"room:{room_id}")
