from app.auth import bp
from app.models import Users, Stack
from flask import jsonify, request, Response
from app import db
from app.utils.errors import bad_request


@bp.route('/register', methods=['POST'])
def register() -> Response:
    '''Регистрация соискателя на платформе'''
    data = request.json or {}
    if 'email' not in data or 'password' not in data:
        return bad_request('must include email and password fields')
    if Users.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = Users(email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    token = user.get_token()
    return jsonify({'access_token': token})


@bp.route('/login', methods=['POST'])
def login() -> Response:
    '''авторизация соискателя на платформе'''
    data = request.json or {}
    if 'email' not in data or 'password' not in data:
        return bad_request('must include email and password fields')
    user = Users.authenticate(email=data['email'], password=data['password'])
    if user:
        token = user.get_token()
        # Временный скрипт, который создает стэк
        stack = Stack.query.all()
        if not stack:
            stack = Stack(names='python/sql/pandas')
            db.session.add(stack)  # Далее это надо будет убрать
            db.session.commit()
        return jsonify({'access_token': token, 'employee': user.employee})
    else:
        return bad_request('wrong password')