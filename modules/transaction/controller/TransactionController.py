from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

from helper import is_auth
from modules.transaction.entity import Transaction
from modules.transaction.form import BalanceTopup
from modules.transaction.form.BalanceTransfer import BalanceTransfer
from modules.user.entity import User

transaction_controller = Blueprint('transaction_controller', __name__)


@transaction_controller.route('/balance_topup', methods=['POST'])
@jwt_required()
def topup_balance():
    current_user = User().find_by_auth_token(get_jwt_identity())
    is_auth(current_user)

    balance_topup = BalanceTopup()
    transaction = balance_topup.load_request(current_user, request.json)
    transaction.save()

    return jsonify(message="Topup successful")


@transaction_controller.route('/transfer', methods=['POST'])
@jwt_required()
def transfer_balance():
    current_user = User().find_by_auth_token(get_jwt_identity())
    is_auth(current_user)

    balance_transfer = BalanceTransfer()
    transaction = balance_transfer.load_request(current_user, request.json)
    transaction.save()

    return make_response(jsonify(message="Transfer success"), 204)


@transaction_controller.route('/top_transactions_per_user', methods=['GET'])
@jwt_required()
def top_transactions_per_user():
    current_user = User().find_by_auth_token(get_jwt_identity())
    is_auth(current_user)

    users = Transaction().get_top_transaction_per_user()

    responses = []
    for user in users: responses.append({"username": user[0], "amount": float(user[1]) + float(user[2])})

    return jsonify(responses)


@transaction_controller.route('/top_users', methods=['GET'])
@jwt_required()
def top_debit_transaction_value():
    current_user = User().find_by_auth_token(get_jwt_identity())
    is_auth(current_user)

    users = Transaction().get_top_debit_transaction_value()

    responses = []
    for user in users: responses.append({"username": user[0], "transacted_value": float(user[1])})

    return jsonify(responses)
