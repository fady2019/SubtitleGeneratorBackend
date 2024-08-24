from flask import Blueprint, request, g
from flasgger import swag_from

from routes.subtitles.segments.segments import segments_blueprint
from services.subtitles import SubtitlesService
from response.response import Response
from response.response_messages import ResponseMessage
from decorators.security.auth_token import validate_token
from decorators.input_validator import input_validator
from decorators.input_validator.input_source import RequestViewArgs, RequestJson
from decorators.security.user_subtitle import validate_user_subtitle
from validation.subtitles import subtitle_id_validator, edit_subtitle_validator
from swagger import get_swagger_doc_path

subtitle_blueprint = Blueprint("subtitle", __name__, url_prefix="/<subtitle_id>")

subtitles_service = SubtitlesService()


@swag_from(get_swagger_doc_path("subtitles", "fetch_subtitle.yml"))
@subtitle_blueprint.get("/")
@validate_token()
@input_validator(input_source=RequestViewArgs(), validator=subtitle_id_validator)
def get_subtitle(subtitle_id):
    user_id = g.user["id"]
    subtitle_data = subtitles_service.fetch_subtitle(user_id, subtitle_id)
    return Response(ResponseMessage.SUCCESSFUL_SUBTITLE_FETCHING, subtitle_data)


@swag_from(get_swagger_doc_path("subtitles", "cancel_generation.yml"))
@subtitle_blueprint.delete("/cancel-generation")
@validate_token()
@input_validator(input_source=RequestViewArgs(), validator=subtitle_id_validator)
@validate_user_subtitle(get_user_id=lambda: g.user["id"], get_subtitle_id=lambda: request.view_args["subtitle_id"])
def cancel_subtitle_generation(subtitle_id):
    subtitles_service.cancel_subtitle_generation(g.user_subtitle)
    return Response(ResponseMessage.SUCCESSFUL_SUBTITLE_GENERATION_CANCELING)


@swag_from(get_swagger_doc_path("subtitles", "rebegin_generation.yml"))
@subtitle_blueprint.post("/rebegin-generation")
@validate_token()
@input_validator(input_source=RequestViewArgs(), validator=subtitle_id_validator)
@validate_user_subtitle(get_user_id=lambda: g.user["id"], get_subtitle_id=lambda: request.view_args["subtitle_id"])
def rebegin_subtitle_generation(subtitle_id):
    subtitles_service.regenerate_subtitle(g.user_subtitle)
    return Response(ResponseMessage.SUCCESSFUL_SUBTITLE_GENERATION_REBEGINNING)


@swag_from(get_swagger_doc_path("subtitles", "edit_subtitle.yml"))
@subtitle_blueprint.put("/edit")
@validate_token()
@input_validator(input_source=RequestViewArgs(), validator=subtitle_id_validator)
@input_validator(input_source=RequestJson(), validator=edit_subtitle_validator)
@validate_user_subtitle(get_user_id=lambda: g.user["id"], get_subtitle_id=lambda: request.view_args["subtitle_id"])
def edit_subtitle(subtitle_id):
    subtitle_data = subtitles_service.edit_subtitle(g.user_subtitle, request.json)
    return Response(ResponseMessage.SUCCESSFUL_SUBTITLE_EDITING, subtitle_data)


@swag_from(get_swagger_doc_path("subtitles", "delete_subtitle.yml"))
@subtitle_blueprint.delete("/delete")
@validate_token()
@input_validator(input_source=RequestViewArgs(), validator=subtitle_id_validator)
@validate_user_subtitle(get_user_id=lambda: g.user["id"], get_subtitle_id=lambda: request.view_args["subtitle_id"])
def delete_subtitle(subtitle_id):
    subtitles_service.delete_subtitle(g.user_subtitle)
    return Response(ResponseMessage.SUCCESSFUL_SUBTITLE_DELETION)


subtitle_blueprint.register_blueprint(segments_blueprint)
