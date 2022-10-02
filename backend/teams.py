from flask import Flask, jsonify, request
from http import HTTPStatus
from uuid import uuid4

app = Flask(__name__)


teams = []

@app.post('/api/teams/')
def add_team():
    payload = request.json
    payload["uid"] = len(teams)+1
    teams.append(payload)
    return payload, 201

@app.get('/api/teams/')
def get_teams():
    return teams, 200

@app.get('/api/teams/<int:uid>')
def get_team_by_id(uid):
    return teams[uid-1], 200

@app.put('/api/teams/<int:uid>')
def update_by_id(uid):
    payload = request.json
    for key in payload:
        teams[uid][key] = payload[key]
    return teams[uid]


@app.delete('/api/teams/<int:uid>')
def delete_team(uid):
    return teams.pop(uid), 201

