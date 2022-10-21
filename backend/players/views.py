from flask import Blueprint, request

from backend.errors import AppError
from backend.players.schemas import Player
from backend.players.storages import OnlineStorage

player_view = Blueprint('player', __name__)


storage = OnlineStorage()


@player_view.get('/')
def get_all():
    players = storage.get_all()
    return [player.dict() for player in players], 200


@player_view.get('/<int:uid>')
def get_by_id(uid):
    player = storage.get_by_id(uid)
    return player.dict(), 200


@player_view.post('/')
def add_player():
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    player = Player(**payload)
    player = storage.add(player)
    return player.dict(), 201


@player_view.put('/<int:uid>')
def update_by_id(uid):
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = uid
    player = Player(**payload)
    player = storage.update(uid, player)
    return player.dict(), 200


@player_view.delete('/<int:uid>')
def delete_player(uid):
    storage.delete(uid)
    return {}, 204
