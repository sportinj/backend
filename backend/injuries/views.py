from flask import Blueprint, request

from backend.errors import AppError
from backend.injuries.schemas import Injury
from backend.injuries.storages import InjuryStorage

injury_view = Blueprint('injury', __name__)

storage = InjuryStorage()


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
    return injury.dict(), 201
