import os
from http import HTTPStatus

from flask import request
from flask_cors import cross_origin
from wsgi import app

from app.controllers.hodler import HodlerController
from app.controllers.token import TokenController
from app.controllers.watcher import WatcherController
from app.tasks.blockchain import (
    blockchain_events_sync_all_contracts,
    blockchain_events_sync_one_contract,
)
from app.utils.session import SessionManager

db_uri = os.environ.get('DATABASE_URL', None)
if not db_uri:
    app.logger.error('DATABASE_URL is not set')
SessionManager.configure(db_uri)


@app.route('/api/tokens', methods=['POST'])
@cross_origin()
def create_tokens():
    payload = request.json
    app.logger.info(f'Token Creation Request: {payload["name"]}')
    token_ctl = TokenController()
    token_ctl.create_token(payload)
    return {'code': HTTPStatus.CREATED}


@app.route('/api/tokens/edit', methods=['POST'])
@cross_origin()
def update_token():
    payload = request.json
    token_ctl = TokenController()
    token_ctl.edit_token(payload)
    return {'code': HTTPStatus.OK}


@app.route('/api/hodlers', methods=['GET'])
@cross_origin()
def get_top_hodlers():
    token_name = request.args.get('token')
    limit = int(request.args.get('limit', 100))
    hodler_ctl = HodlerController()
    hodlers = hodler_ctl.find_top_hodler_by_token_name(token_name, limit)
    return {'code': HTTPStatus.OK, 'hodlers': hodlers}


@app.route('/api/tokens', methods=['GET'])
@cross_origin()
def get_tokens():
    token_ctl = TokenController()
    tokens = token_ctl.get_tokens()
    return {'code': HTTPStatus.OK, 'tokens': [token.to_dict() for token in tokens]}


@app.route('/api/blockchain_sync', methods=['POST'])
@cross_origin()
def blockchain_sync():
    blockchain_events_sync_all_contracts.apply()
    return {'code': HTTPStatus.ACCEPTED}


@app.route('/api/watchers', methods=['POST'])
@cross_origin()
def upsert_watcher():
    payload = request.json
    app.logger.info(f'Watcher Upsert Request: {payload["address"]}')
    watcher_ctl = WatcherController()
    watcher_ctl.upsert_watcher(payload)
    return {'code': HTTPStatus.CREATED}


@app.route('/api/tokens/sync', methods=['POST'])
@cross_origin()
def sync_token():
    payload = request.json
    token_ctl = TokenController()
    token = token_ctl.get_token_by_name(payload['name'])
    blockchain_events_sync_one_contract.apply(args=[token.to_dict()])
    return {'code': HTTPStatus.ACCEPTED}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
