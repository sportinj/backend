from backend.database import db_session
from backend.errors import NotFoundError
from backend.models import Player
from backend.players.schemas import Player as PlayerSchema


class LocalStorage:
    def __init__(self):
        self.players: dict[int, PlayerSchema] = {}
        self.last_uid = 0

    def add(self, player: PlayerSchema) -> PlayerSchema:
        self.last_uid += 1
        player.uid = self.last_uid
        self.players[self.last_uid] = player
        return player

    def get_all(self) -> list[PlayerSchema]:
        return list(self.players.values())

    def get_by_id(self, uid: int) -> PlayerSchema:
        if uid not in self.players:
            raise NotFoundError('players', uid)

        return self.players[uid]

    def update(self, uid: int, player: PlayerSchema) -> PlayerSchema:
        if uid not in self.players:
            raise NotFoundError('player', uid)

        self.players[uid] = player
        return player

    def delete(self, uid: int) -> None:
        if uid not in self.players:
            raise NotFoundError('players', uid)
        self.players.pop(uid)


class OnlineStorage(LocalStorage):
    def add(self, player: PlayerSchema) -> PlayerSchema:
        entity = Player(name=player.name, description=player.description)

        db_session.add(entity)
        db_session.commit()

        return PlayerSchema(uid=entity.uid, name=entity.name, description=entity.description)
