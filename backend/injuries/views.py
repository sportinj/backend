from http import HTTPStatus

import orjson
from flask import Blueprint, Response, request

from backend.errors import AppError
from backend.injuries.schemas import Injury
from backend.injuries.storages import InjuryStorage

injury_view = Blueprint('injury', __name__)

storage = InjuryStorage()


@injury_view.get('/<int:player_id>/injuries/')
def get_for_player(player_id: int):
    entities = storage.get_for_player(player_id)
    injuries = [Injury.from_orm(entity) for entity in entities]
    return Response(
        response=orjson.dumps([injury.dict() for injury in injuries]),
        status=HTTPStatus.OK,
        content_type='application/json',
    )


@injury_view.post('/<int:player_id>/injuries/')
def add(player_id: int):
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    injury = Injury(**payload)
    entity = storage.add(
        description=injury.description,
        name=injury.name,
        start_date=injury.start_date,
        end_date=injury.end_date,
        player_id=player_id,
    )
    injury = Injury.from_orm(entity)
    return Response(
        response=orjson.dumps(injury.dict()),
        status=HTTPStatus.CREATED,
        content_type='application/json',
    )
