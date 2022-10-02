from flask import Flask, jsonify, request
from http import HTTPStatus
from uuid import uuid4
from typing import Any

app = Flask(__name__)

Json = dict[int, str|int]
class Storage:
    def __init__(self):
        self.teams: dict[int, Json] = {}
        self.last_uid = 0

    def add(self, team: Json) -> Json :
        self.last_uid +=1
        team["uid"] = self.last_uid
        self.teams[self.last_uid] = team
        return team

    def get_teams(self) -> list[Json]:
        return list(self.teams.values())

    def get_team_by_id(self, uid:int) ->Json:
        return self.teams[uid]

    def update_by_id(self, uid:int, team: Json) ->Json:
        self.teams[uid] = team
        return team

    def delete(self, uid: int) -> None:
        self.teams.pop(uid)




storage = Storage()


@app.post('/api/teams/')
def add_team():
    team = request.json
    return storage.add(team), 201

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

