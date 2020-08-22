import os
from http import HTTPStatus

from flask import Flask, request

from app.controllers.token import TokenController
from app.utils.session import SessionManager

app = Flask(__name__)
db_uri = os.environ.get('DATABASE_URI', None)
if not db_uri:
    app.logger.error('DATABASE_URI is not set')
SessionManager.configure(db_uri)


@app.route('/tokens', methods=['POST'])
def create_tokens():
    payload = request.form
    app.logger.info(f'Token Creation Request: {payload["name"]}')
    token_ctl = TokenController()
    token_ctl.create_token(payload)
    return {'code': HTTPStatus.CREATED}
