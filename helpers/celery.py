import redis, os


redis_client = redis.StrictRedis.from_url(url=os.getenv("REDIS_URL"))


def mark_task_as_invoked(task_id: str):
    redis_client.sadd("celery_invoked_tasks", task_id)


def remove_invoked_task(task_id: str):
    redis_client.srem("celery_invoked_tasks", task_id)


def is_invoked(task_id: str):
    return bool(redis_client.sismember("celery_invoked_tasks", task_id))
