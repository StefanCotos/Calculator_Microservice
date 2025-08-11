import json
from datetime import datetime
from app.core.redis_cache import redis_client


async def publish_request_event(data: dict):
    """
    Publishes a calculation request event to the 'calc_requests' Redis stream.
    If the 'timestamp' key is not present in the input data, it adds the current UTC timestamp.
    The data is serialized to JSON and published to the Redis stream using the 'xadd' command.
    Args:
        data (dict): The request data to be published.
            Should contain relevant calculation request information.
    Raises:
        Any exceptions raised by the Redis client during publishing.
    """

    if "timestamp" not in data:
        data["timestamp"] = datetime.utcnow().isoformat()
    await redis_client.xadd("calc_requests", {"data": json.dumps(data)})
