from flask import g
from functools import wraps
from typing import Callable

from db.repositories.subtitle import SubtitleRepository
from response.response import Response
from response.response_messages import ResponseMessage
from dtos_mappers.subtitle import SubtitleWithTaskIdMapper

subtitle_repo = SubtitleRepository()


def validate_user_subtitle(get_user_id: Callable[[], str], get_subtitle_id: Callable[[], str]):
    """
    - validate that the current user owns the target subtitle
    - store the target subtitle in g.user_subtitle
    """

    def decorator(f: Callable[..., Response]):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_user_id()
            subtitle_id = get_subtitle_id()

            subtitle = subtitle_repo.find(
                filter=lambda Subtitle: (Subtitle.id == subtitle_id) & (Subtitle.user_id == user_id),
                options={
                    "throw_if_not_found": True,
                    "error_msg": ResponseMessage.FAILED_USER_HAS_NO_SUBTITLE_WITH_ID,
                    "return_first": True,
                },
            )

            g.user_subtitle = SubtitleWithTaskIdMapper().to_dto(subtitle)

            return f(*args, **kwargs)

        return decorated_function

    return decorator
