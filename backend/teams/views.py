from flask import Blueprint, request
from itsdangerous import TimestampSigner
from pydantic import ValidationError

from backend.errors import AppError
from backend.players.storages import OnlineStorage as PlayerStorage
from backend.teams.schemas import Team
from backend.teams.storages import OnlineStorage

team_view = Blueprint('teams', __name__)

storage = OnlineStorage()
player_storage = PlayerStorage()


@team_view.post('/')
def add_team():
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1

    team = Team(**payload)

    team = storage.add(team)
    return team.dict(), 201


@team_view.get('/')
def get_all():
    teams = storage.get_all()

    return [team.dict() for team in teams], 200




@team_view.get('/<int:uid>')
def get_team_by_id(uid):
    team = storage.get_by_id(uid)
    return team.dict(), 200


@team_view.put('/<int:uid>')
def update(uid):
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    team = Team(**payload)
    team = storage.update(uid, team)
    return team.dict(), 200


@team_view.delete('/<int:uid>')
def delete_team(uid):
    storage.delete(uid)
    return {}, 204

@team_view.get('/<int:uid>/players/')
def get_all_players(uid, name=''):
    if 'name' in request.args:
        name = request.args.get('name')
        players = player_storage.find_for_team(uid, name)
    else:
        players = player_storage.get_for_team(uid)

    return [player.dict() for player in players], 200
