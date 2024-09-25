from typing import Optional
import redis, os, json

from global_types.subtitle_task import TSubtitleTaskMetadata

redis_client = redis.StrictRedis.from_url(url=os.getenv("REDIS_URL"))
redis_dir_name = "subtitle_task_metadata"


def set_subtitle_task_metadata(subtitle_id: str, metadata: TSubtitleTaskMetadata):
    metadata = {
        **get_subtitle_task_metadata(subtitle_id, {}),
        **metadata,
    }

    redis_client.hset(redis_dir_name, subtitle_id, json.dumps(metadata))


def get_subtitle_task_metadata(subtitle_id: str, default=None) -> Optional[TSubtitleTaskMetadata]:
    metadata = redis_client.hget(redis_dir_name, subtitle_id)

    if not metadata:
        return default

    return json.loads(metadata)


def remove_subtitle_task_metadata(subtitle_id: str):
    redis_client.hdel(redis_dir_name, subtitle_id)
