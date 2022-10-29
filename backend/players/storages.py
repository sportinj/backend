from sqlalchemy.exc import IntegrityError

from backend.database import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import Player, Team


class OnlineStorage:
    name = 'players'

    def add(self, name: str, description: str, team_id: int, status: str) -> Player:
        entity = Player(
            name=name,
            description=description,
            team_id=team_id,
            status=status,
        )
        try:
            db_session.add(entity)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return entity

    def update(self, uid: int, name: str, description: str, status: str) -> Player:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        entity.name = name
        entity.description = description
        entity.status = status

        db_session.commit()

        return entity

    def delete(self, uid: int) -> None:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        db_session.delete(entity)
        db_session.commit()

    def get_by_id(self, uid: int) -> Player:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        return entity

    def get_all(self) -> list[Player]:
        return Player.query.all()

    def get_for_team(self, uid: int) -> list[Player]:
        team = Team.query.get(uid)

        if not team:
            raise NotFoundError('teams', uid)

        return team.players

    def find_by_name(self, name: str) -> list[Player]:
        search = '{name}%'.format(name=name)

        return Player.query.filter(Player.name.ilike(search)).all()

    def find_for_team(self, uid: int, name: str) -> list[Player]:
        return Player.query.filter(
            Player.team_id == uid,
            Player.name == name,
        ).all()
