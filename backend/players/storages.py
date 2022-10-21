from sqlalchemy.exc import IntegrityError

from backend.database import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import Player, Team
from backend.players.schemas import Player as PlayerSchema


class OnlineStorage:
    name = 'players'

    def add(self, player: PlayerSchema) -> PlayerSchema:
        entity = Player(
            name=player.name,
            description=player.description,
            team_id=player.team_id
        )
        
        try:
            db_session.add(entity)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return PlayerSchema(
            uid=entity.uid,
            name=entity.name,
            description=player.description,
            team_id=player.team_id
        )

    def update(self, uid: int, player: PlayerSchema) -> PlayerSchema:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        entity.name = player.name
        entity.description = player.description

        db_session.commit()

        return PlayerSchema(
            uid=entity.uid,
            name=entity.name,
            description=player.description,
            team_id=player.team_id
        )

    def delete(self, uid: int) -> None:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        db_session.delete(entity)
        db_session.commit()


    def get_by_id(self, uid: int) -> PlayerSchema:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        return PlayerSchema(
            uid=entity.uid,
            name=entity.name,
            description=entity.description,
            team_id=entity.team_id
        )

    def get_all(self) -> list[PlayerSchema]:
        entities = Player.query.all()
        all_players = []

        for player in entities:
            poi = PlayerSchema(
                uid=player.uid,
                name=player.name,
                description=player.description,
                team_id=player.team_id
            )

            all_players.append(poi)

        return all_players

    def get_for_team(self, uid: int) -> list[PlayerSchema]:
        team = Team.query.get(uid)

        if not team:
            raise NotFoundError('teams', uid)

        entities = team.players

        all_players = []

        for player in entities:
            poi = PlayerSchema(
                uid=player.uid,
                name=player.name,
                description=player.description,
                team_id=player.team_id
            )

            all_players.append(poi)

        return all_players

    def find_for_team(self, uid: int, name: str) -> list[PlayerSchema]:
        search = '%{}%'.format(name)
        entities = Player.query.filter(
            Player.team_id == uid,
            Player.name.ilike(search),
        ).all()

        target_players = []

        if not entities:
            raise NotFoundError(name, uid)

        for entity in entities:
            player = PlayerSchema(
                uid=entity.uid,
                name=entity.name,
                description=entity.description,
                team_id=entity.team_id
            )

            target_players.append(player)

        return target_players
