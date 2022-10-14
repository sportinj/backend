from flask import Blueprint, request
from pydantic import ValidationError

from backend.errors import AppError
from backend.teams.schemas import Team
from backend.teams.storages import OnlineStorage

team_view = Blueprint('teams', __name__)

storage = OnlineStorage()


@team_view.post('/')
def add_team():
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    try:
        team = Team(**payload)
    except ValidationError as err:
        return {'error': str(err)}, 400

    team = storage.add(team)
    return team.dict(), 201


@team_view.get('/')
def get_teams():
    teams = storage.get_teams()
    return [team.dict() for team in teams], 200


@team_view.get('/<int:uid>')
def get_team_by_id(uid):
    team = storage.get_team_by_id(uid)
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
