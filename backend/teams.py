from flask import Flask, jsonify, request
from http import HTTPStatus
from uuid import uuid4
from typing import Any
from pydantic import BaseModel, ValidationError



app = Flask(__name__)

Json = dict[int, str|int]

class Team(BaseModel):
    uid: int
    name: str

class LocalStorage:
    def __init__(self):
        self.teams: dict[int, Team] = {}
        self.last_uid = 0

    def add(self, team: Team) -> Team :
        self.last_uid +=1
        team.uid = self.last_uid
        self.teams[self.last_uid] = team
        return team

    def get_teams(self) -> list[Team]:
        return list(self.teams.values())

    def get_team_by_id(self, uid:int) ->Team:
        return self.teams[uid]

    def update_by_id(self, uid:int, team: Team) ->Team:
        self.teams[uid] = team
        return team

    def delete(self, uid: int) -> None:
        self.teams.pop(uid)




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
    return storage.get_teams(), 200

@app.get('/api/teams/<int:uid>')
def get_team_by_id(uid):
    return storage.get_team_by_id(uid), 200

@app.put('/api/teams/<int:uid>')
def update_by_id(uid):
    team = request.json
    return storage.update_by_id(uid, team), 200


@app.delete('/api/teams/<int:uid>')
def delete_team(uid):
    storage.delete(uid)
    return {}, 204

