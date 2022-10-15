from backend.database import db_session
from backend.errors import NotFoundError
from backend.models import Team
from backend.teams.schemas import Team as TeamSchema


class OnlineStorage():
    def add(self, team: TeamSchema) -> TeamSchema:
        entity = Team(name=team.name, description=team.description)

        db_session.add(entity)
        db_session.commit()

        return TeamSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def update(self, uid: int, team: TeamSchema) -> TeamSchema:
        entity = Team.query.get(uid)

        if not entity:
            raise NotFoundError('teams', uid)

        entity.name = team.name
        entity.description = team.description

        db_session.commit()

        return TeamSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def delete(self, uid: int) -> None:
        entity = Team.query.get(uid)

        if not entity:
            raise NotFoundError('teams', uid)

        db_session.delete(entity)
        db_session.commit()

    def get_by_id(self, uid: int) -> TeamSchema:
        entity = Team.query.get(uid)

        if not entity:
            raise NotFoundError('teams', uid)

        return TeamSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def get_all(self) -> list[TeamSchema]:
        entities = Team.query.all()

        return [
            TeamSchema(uid=entity.uid, name=entity.name, description=entity.description)
            for entity in entities
        ]
