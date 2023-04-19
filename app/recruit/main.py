from app.recruit import bp
from app.models import Users, Stack
from flask import jsonify, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.utils.errors import bad_request


@bp.route('/stacks', methods=['GET'])
def get_stacks() -> Response:
    '''Возвращает все существующие стэки'''
    stacks = Stack.query.all()
    payload = [{'stack_id': i.id, 'stack': i.names} for i in stacks]
    return jsonify(payload)


@bp.route('/users', methods=['POST'])
def get_users() -> Response:
    '''Выгружает соскателей по стеку, далее разбивает их на классы в зависимости от рэйтинга'''
    data = request.json or {}
    if 'stack_id' not in data:
        return bad_request('must include stack_id field')
    users = Users.get_users(stack_id=data['stack_id'])
    high = []
    mid = []
    low = []
    for i in users:
        if i.rate >= 7:
            high.append({
                'id': i.id, 'name': i.name, 'surname': i.surname, 'age': i.age, 'city': i.city,
                'tlg_link': i.tlg_link, 'resume': i.resume, 'rate': i.rate
            })
        elif 3 <= i.rate < 7:
            mid.append({
                'id': i.id, 'name': i.name, 'surname': i.surname, 'age': i.age, 'city': i.city,
                'tlg_link': i.tlg_link, 'resume': i.resume, 'rate': i.rate
            })
        else:
            low.append({
                'id': i.id, 'name': i.name, 'surname': i.surname, 'age': i.age, 'city': i.city,
                'tlg_link': i.tlg_link, 'resume': i.resume, 'rate': i.rate
            })
    classes = dict(zip(['high', 'mid', 'low'], [high, mid, low]))
    return jsonify(classes)
