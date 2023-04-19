from app.user import bp
from app.models import Users
from flask import jsonify, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.utils import hard_tests
from app.utils.errors import bad_request


@bp.route('/update_data', methods=['POST'])
@jwt_required()
def update_data() -> Response:
    '''Обновляет данные пользователя после отправки анкеты'''
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    data = request.json or {}
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify({'id': user.id})


@bp.route('/hard_test', methods=['GET'])
@jwt_required()
def hard_test() -> Response:
    '''Возвращает JSON с тестом по стеку юзера'''
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    if user.stack_id == 1:
        return jsonify(hard_tests.hard_tests[user.stack_id])
    else:
        return jsonify({'других тестов пока нет': 200})


@bp.route('/soft_test', methods=['GET'])
@jwt_required()
def soft_test() -> Response:
    '''Возвращает JSON с тестом по софт навыкам. Один для всех юзеров'''
    return jsonify(hard_tests.quiz_soft)


@bp.route('/get_hard_rate', methods=['POST'])
@jwt_required()
def get_hard_rate() -> Response:
    '''Подсчитываем количетво набранных баллов на тесте хард навыков'''
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    data = request.json or {}
    if len(data) != len(hard_tests.hard_tests[user.stack_id]):
        return bad_request('Ответов на вопросы меньше чем вопросов')
    rate = 0
    for ans in data.values():
        if ans['correct_answer'] == ans['users_answer']:
            rate += 1
    user.hard_rate = rate
    db.session.commit()
    return jsonify({'rate': rate})


@bp.route('/get_soft_rate', methods=['POST'])
@jwt_required()
def get_soft_rate() -> Response:
    '''Подсчитываем количетво набранных баллов на тесте софт навыков'''
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first_or_404()
    data = request.json or {}
    if len(data) != len(hard_tests.quiz_soft):
        return bad_request('Ответов на вопросы меньше чем вопросов')
    rate = 0
    for ans in data.values():
        if ans['correct_answer'] == ans['users_answer']:
            rate += 1
    user.soft_rate = rate
    db.session.commit()
    return jsonify({'rate': rate})


