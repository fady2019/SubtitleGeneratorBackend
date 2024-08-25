from flask import Blueprint, request, g, send_file
from flasgger import swag_from

from routes.subtitles.segments.segment import segment_blueprint
from services.segments import SegmentsService
from response.response import Response
from response.response_messages import ResponseMessage
from decorators.input_validator import input_validator
from decorators.input_validator.input_source import RequestArgs, RequestViewArgs
from decorators.security.auth_token import validate_token
from decorators.security.user_subtitle import validate_user_subtitle
from validation.subtitles import subtitle_id_validator, subtitle_file_type_validator
from validation.pagination import pagination_validator
from swagger import get_swagger_doc_path


segments_blueprint = Blueprint("segments", __name__, url_prefix="/segments")

segments_service = SegmentsService()


@swag_from(get_swagger_doc_path("subtitles", "segments", "fetch_segments.yml"))
@segments_blueprint.get("/")
@validate_token()
@input_validator(input_source=RequestViewArgs(), validator=subtitle_id_validator)
@input_validator(input_source=RequestArgs(), validator=pagination_validator)
@validate_user_subtitle(get_user_id=lambda: g.user["id"], get_subtitle_id=lambda: request.view_args["subtitle_id"])
def fetch_segments(subtitle_id):
    page = request.args.get("page", None)
    items_per_page = request.args.get("items_per_page", None)
    segments_data = segments_service.fetch_segments(subtitle_id, page=page, items_per_page=items_per_page)
    return Response(ResponseMessage.SUCCESSFUL_SEGMENTS_FETCHING, segments_data)


@swag_from(get_swagger_doc_path("subtitles", "segments", "as_file.yml"))
@segments_blueprint.get("/as-file")
@validate_token()
@input_validator(input_source=RequestViewArgs(), validator=subtitle_id_validator)
@input_validator(input_source=RequestArgs(), validator=subtitle_file_type_validator)
@validate_user_subtitle(get_user_id=lambda: g.user["id"], get_subtitle_id=lambda: request.view_args["subtitle_id"])
def as_file(subtitle_id):
    subtitle = g.user_subtitle
    file_type = request.args.get("file_type")
    byte_file, mimetype = segments_service.create_file(subtitle, file_type)
    download_name = f"{subtitle["title"]}.{file_type}"
    return send_file(byte_file, as_attachment=True, download_name=download_name, mimetype=mimetype)


segments_blueprint.register_blueprint(segment_blueprint)