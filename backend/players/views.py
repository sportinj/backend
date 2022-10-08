from flask import Flask, request
from pydantic import  ValidationError
from backend.players.schemas import Player
from backend.players.storages import LocalStorage
from backend.errors import AppError

app = Flask(__name__)

def handle_app_error(e: AppError):
    return {'error': str(e)}, e.code

def handle_validation_error(e: ValidationError):
    return {'error': str(e)}, 422

app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(ValidationError, handle_validation_error)

storage = LocalStorage()

@app.get('/api/players/')
def get_all():
    players = storage.get_all()
    return [player.dict() for player in players], 200

@app.get('/api/players/<int:uid>')
def get_player_by_id(uid):
    player = storage.get_by_id(uid)
    return player.dict(), 200

@app.post('/api/players/')
def add_player():
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    player = Player(**payload)
    player = storage.add(player)
    return player.dict(), 201

@app.put('/api/players/<int:uid>')
def update_by_id(uid):
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    player = Player(**payload)
    player = storage.update(uid, player)
    return player.dict(), 200

@app.delete('/api/players/<int:uid>')
def delete_player(uid):
    storage.delete(uid)
    return {}, 204

