import redis
import json


class SentinelProducer:
    def __init__(self, host='redis', port=6379):
        # Use 'redis' as the host because that is the service name in docker-compose
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def enqueue_job(self, asset_id, image_path):
        """
        Pushes a task to the 'ocr_tasks' queue in Redis.
        """
        payload = {
            "asset_id": str(asset_id),
            "image_path": image_path
        }

        # We use LPUSH to create a FIFO (First-In, First-Out) queue
        self.client.lpush("ocr_tasks", json.dumps(payload))
        print(f"Task enqueued: {asset_id}")