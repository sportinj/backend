from backend.errors import NotFoundError
from backend.players.schemas import Player


class LocalStorage:
    def __init__(self):
        self.players: dict[int, Player] = {}
        self.last_uid = 0

    def add(self, player: Player) -> Player:
        self.last_uid += 1
        player.uid = self.last_uid
        self.players[self.last_uid] = player
        return player

    def get_all(self) -> list[Player]:
        return list(self.players.values())

    def get_by_id(self, uid: int) -> Player:
        if uid not in self.players:
            raise NotFoundError('players', uid)

        return self.players[uid]

    def update(self, uid: int, player: Player) -> Player:
        if uid not in self.players:
            raise NotFoundError('player', uid)

        self.players[uid] = player
        return player

    def delete(self, uid: int) -> None:
        if uid not in self.players:
            raise NotFoundError('players', uid)
        self.players.pop(uid)
