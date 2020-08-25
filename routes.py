import os
from http import HTTPStatus

from flask import Flask, request
from flask_cors import CORS, cross_origin

from app.controllers.hodler import HodlerController
from app.controllers.token import TokenController
from app.utils.session import SessionManager

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADES'] = 'Content-Type'

db_uri = os.environ.get('DATABASE_URL', None)
if not db_uri:
    app.logger.error('DATABASE_URL is not set')
SessionManager.configure(db_uri)


@app.route('/tokens', methods=['POST'])
@cross_origin()
def create_tokens():
    payload = request.form
    app.logger.info(f'Token Creation Request: {payload["name"]}')
    token_ctl = TokenController()
    token_ctl.create_token(payload)
    return {'code': HTTPStatus.CREATED}


@app.route('/hodlers', methods=['GET'])
@cross_origin()
def get_top_hodlers():
    token_name = request.args.get('token')
    limit = int(request.args.get('limit'))
    hodler_ctl = HodlerController()
    hodlers = hodler_ctl.find_top_hodler_by_token_name(token_name, limit)
    return {'code': HTTPStatus.OK, 'hodlers': hodlers}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
