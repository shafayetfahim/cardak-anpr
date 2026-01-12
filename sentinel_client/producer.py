import redis
import json
import os

class SentinelProducer:
    def __init__(self, host=None, port=6379):
        self.host = host or os.getenv('REDIS_HOST', 'localhost')
        self.client = redis.Redis(host=self.host, port=port, decode_responses=True)

    def enqueue_job(self, asset_id, image_path):
        payload = {
            "asset_id": str(asset_id),
            "image_path": image_path
        }
        self.client.lpush("ocr_tasks", json.dumps(payload))
        print(f"Task enqueued: {asset_id}")