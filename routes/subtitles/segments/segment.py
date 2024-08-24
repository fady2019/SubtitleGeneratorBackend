from flask import Blueprint, request, g
from flasgger import swag_from

from services.segments import SegmentsService
from response.response import Response
from response.response_messages import ResponseMessage
from decorators.input_validator import input_validator
from decorators.input_validator.input_source import RequestViewArgs, RequestJson
from decorators.security.auth_token import validate_token
from decorators.security.user_subtitle import validate_user_subtitle
from validation.subtitles import subtitle_id_validator, subtitle_segment_id_validator, edit_subtitle_segment_validator
from swagger import get_swagger_doc_path


segment_blueprint = Blueprint("segment", __name__, url_prefix="/<int:segment_id>")

segments_service = SegmentsService()


@swag_from(get_swagger_doc_path("subtitles", "segments", "edit_segment.yml"))
@segment_blueprint.put("/edit")
@validate_token()
@input_validator(input_source=RequestViewArgs(), validator=subtitle_id_validator)
@input_validator(input_source=RequestViewArgs(), validator=subtitle_segment_id_validator)
@input_validator(input_source=RequestJson(), validator=edit_subtitle_segment_validator)
@validate_user_subtitle(get_user_id=lambda: g.user["id"], get_subtitle_id=lambda: request.view_args["subtitle_id"])
def edit_segment(subtitle_id, segment_id):
    segment_data = segments_service.edit_segment(subtitle_id, segment_id, request.json)
    return Response(ResponseMessage.SUCCESSFUL_SEGMENT_EDITING, segment_data)
