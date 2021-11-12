from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from helper import is_auth
from modules.user.entity import User
from modules.user.form import BasicSignUp

account_controller = Blueprint('account_controller', __name__)


@account_controller.route('/create_user', methods=['POST'])
def signup_basic():
    basic_signup = BasicSignUp()
    new_user = basic_signup.load_request(request.json)
    new_user.save()

    return make_response(jsonify(token=create_access_token(identity=new_user.auth_token)), 201)


@account_controller.route('/balance_read', methods=['GET'])
@jwt_required()
def view_balance():
    current_user = User().find_by_auth_token(get_jwt_identity())
    is_auth(current_user)

    return jsonify(balance=current_user.balance)
