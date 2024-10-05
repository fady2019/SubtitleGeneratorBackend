from celery.result import AsyncResult
import redis, os


redis_client = redis.StrictRedis.from_url(url=os.getenv("REDIS_URL"))


def revoke_task(task_id: str):
    result = AsyncResult(task_id)
    result.revoke(terminate=True, signal="SIGKILL")


def mark_task_as_revoked(task_id: str):
    redis_client.sadd("celery_revoked_tasks", task_id)


def remove_revoked_task(task_id: str):
    redis_client.srem("celery_revoked_tasks", task_id)


def is_revoked(task_id: str):
    return bool(redis_client.sismember("celery_revoked_tasks", task_id))
