from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from typing import Optional
from flask import Response


def error_response(status_code: int, message: Optional[str] = None) -> Response:
    '''Создаем респонс ошибки'''
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message: str) -> Response:
    return error_response(400, message)