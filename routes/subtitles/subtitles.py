from flask import Blueprint, request, g
from flasgger import swag_from

from routes.subtitles.subtitle import subtitle_blueprint
from services.subtitles import SubtitlesService
from response.response import Response
from response.response_messages import ResponseMessage
from decorators.security.auth_token import validate_token
from decorators.input_validator import input_validator
from decorators.input_validator.input_source import RequestFiles, RequestForm
from decorators.restrictions.rate_limit import check_limit_rate
from validation.subtitles import subtitle_begin_generation_media_file_validator, subtitle_begin_generation_validator
from swagger import get_swagger_doc_path


subtitles_blueprint = Blueprint("subtitles", __name__, url_prefix="/subtitles")

subtitles_service = SubtitlesService()


@swag_from(get_swagger_doc_path("subtitles", "fetch_subtitles.yml"))
@subtitles_blueprint.get("/")
@validate_token()
def get_subtitles():
    user_id = g.user["id"]
    subtitles = subtitles_service.fetch_subtitles(user_id)
    return Response(ResponseMessage.SUCCESSFUL_SUBTITLES_FETCHING, subtitles)


@swag_from(get_swagger_doc_path("subtitles", "begin_generation.yml"))
@subtitles_blueprint.post("/begin-generation")
@validate_token()
@input_validator(input_source=RequestFiles(), validator=subtitle_begin_generation_media_file_validator)
@input_validator(input_source=RequestForm(), validator=subtitle_begin_generation_validator)
@check_limit_rate(get_user_id=lambda: g.user["id"], timeframe_in_mins=5, max_attempts=1)
def begin_subtitle_generation():
    user_id = g.user["id"]

    data = subtitles_service.generate_subtitle(
        user_id,
        {
            "title": request.form.get("title"),
            "media_file": request.files.get("media_file"),
            "translate": request.form.get("translate").lower() == "true",
        },
    )

    return Response(ResponseMessage.SUCCESSFUL_SUBTITLE_GENERATION_BEGINNING, data)


subtitles_blueprint.register_blueprint(subtitle_blueprint)
