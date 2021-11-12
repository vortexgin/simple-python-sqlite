#!flask/bin/python

from datetime import timedelta

from flask import Flask, make_response, url_for, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config.app import app_debug, secret_key, app_port, app_host, db_path, conn
from exception import BaseException
from helper.SqliteHelper import execute

from modules.user.controller import account_controller
from modules.transaction.controller import transaction_controller

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['JWT_SECRET_KEY'] = secret_key
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=60 * 60)  # 1 hours
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=60 * 60)  # 1 hours
app.register_blueprint(account_controller, url_prefix='/')
app.register_blueprint(transaction_controller, url_prefix='/')

CORS(app)
jwt = JWTManager(app)


def init_db():
    execute(conn, "CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, username text NOT NULL, auth_token text NOT NULL, balance float, created_at integer)")
    execute(conn, "CREATE TABLE IF NOT EXISTS transactions (id integer PRIMARY KEY, type text NOT NULL, amount float, actor integer, recipient integer, status text NOT NULL, created_at integer)")


@app.errorhandler(BaseException)
def custom_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        'description': 'Entity/webpage not found',
        'error': 'Not found',
    }), 404)


@app.errorhandler(500)
def system_error(error):
    return make_response(jsonify({
        'description': 'Application critical error',
        'error': 'System error',
    }), 500)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return 'pong!'


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/sitemap")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, str(rule.methods), rule.endpoint))
        elif rule.endpoint != "static":
            links.append((str(rule), str(rule.methods), rule.endpoint))

    # links is now a list of url, endpoint tuples
    return jsonify(links)


if __name__ == '__main__':
    init_db()
    app.run(debug=app_debug, host=app_host, port=app_port)
