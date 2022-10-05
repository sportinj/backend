from flask import Flask, request
from pydantic import ValidationError
from backend.teams.storages import LocalStorage
from backend.teams.schemas import Team

app = Flask(__name__)

storage = LocalStorage()

@app.post('/api/teams/')
def add_team():
    payload = request.json
    payload["uid"] = -1
    try:
        team = Team(**payload)
    except ValidationError as err:
        return {"error": str(err)}, 400

    team = storage.add(team)
    return team.dict(), 201

@app.get('/api/teams/')
def get_teams():
    teams = storage.get_teams()
    return [team.dict() for team in teams], 200

@app.get('/api/teams/<int:uid>')
def get_team_by_id(uid):
    team = storage.get_team_by_id(uid)
    return team.dict(), 200


@app.put('/api/teams/<int:uid>')
def update(uid):
    payload = request.json
    try:
        team = Team(**payload)
    except ValidationError as err:
        return {"error": str(err)}, 400
    team = storage.update(uid, team)
    return team.dict(), 200


@app.delete('/api/teams/<int:uid>')
def delete_team(uid):
    storage.delete(uid)
    return {}, 204

