from flask import request
from functools import wraps
from typing import Callable
import redis, os, math

from response.response import Response, ResponseError

redis_client = redis.StrictRedis.from_url(url=os.getenv("REDIS_URL"))


def check_limit_rate(get_user_id: Callable[[], str], timeframe_in_mins: float, max_attempts: int):
    """prevent the user from accessing an endpoint in quick succession

    Args:
        get_user_id (Callable[[], str]): a function that returns the current user's id
        timeframe_in_mins (float): how many minutes should elapse before the current user can access the endpoint again
        max_attempts (int): the maximum number of times an endpoint can be accessed by the current user (in the given timeframe)
    """
    if timeframe_in_mins <= 0:
        raise Exception("timeframe_in_mins should be a positive number")

    if max_attempts <= 0 or int(max_attempts) != max_attempts:
        raise Exception("max_attempts should be a positive integer")

    def decorator(f: Callable[..., Response]):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_user_id()
            action_key = f"{request.endpoint}:{user_id}"
            attempts_count = int(redis_client.get(action_key) or 0)

            if attempts_count == max_attempts:
                wait_for = math.ceil(redis_client.ttl(action_key) / 60)

                raise ResponseError(
                    {
                        "msg": f"you have exceeded the maximum number of attempts. please wait {wait_for} minute(s) before trying again",
                        "status_code": 429,
                    }
                )

            response = f(*args, **kwargs)

            attempts_count = redis_client.incr(action_key)

            if attempts_count == 1:
                redis_client.expire(action_key, timeframe_in_mins * 60)

            return response

        return decorated_function

    return decorator
