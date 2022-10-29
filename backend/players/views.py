from flask import Blueprint, request

from backend.errors import AppError
from backend.injuries.views import injury_view
from backend.players.schemas import Player
from backend.players.storages import OnlineStorage

player_view = Blueprint('player', __name__)
player_view.register_blueprint(injury_view, url_prefix='')

storage = OnlineStorage()


@player_view.get('/')
def get_all():
    name = request.args.get('name')
    if name:
        entities = storage.find_by_name(name)
    else:
        entities = storage.get_all()
    players = [Player.from_orm(entity) for entity in entities]
    return [player.dict() for player in players], 200


@player_view.get('/<int:uid>')
def get_by_id(uid):
    entity = storage.get_by_id(uid)
    player = Player.from_orm(entity)
    return player.dict(), 200


@player_view.post('/')
def add_player():
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    player = Player(**payload)
    entity = storage.add(
        name=player.name,
        description=player.description,
        team_id=player.team_id,
        status=player.status,
    )
    player = Player.from_orm(entity)
    return player.dict(), 201


@player_view.put('/<int:uid>')
def update_by_id(uid):
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = uid
    player = Player(**payload)
    entity = storage.update(
        uid,
        name=player.name,
        description=player.description,
        status=player.status,
    )
    player = Player.from_orm(entity)
    return player.dict(), 200


@player_view.delete('/<int:uid>')
def delete_player(uid):
    storage.delete(uid)
    return {}, 204
