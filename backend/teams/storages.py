from backend.database import db_session
from backend.models import Team
from backend.teams.schemas import Team as TeamSchema
from backend.errors import NotFoundError


class OnlineStorage():
    def add(self, team: TeamSchema) -> TeamSchema:
        entity = Team(name=team.name)

        db_session.add(entity)
        db_session.commit()

        return TeamSchema(uid=entity.uid, name=entity.name)

    def update(self, uid: int, team: TeamSchema) -> TeamSchema:
        entity = Team.query.get(uid)

        if not entity:
            raise NotFoundError('teams', uid)

        entity.name = team.name

        db_session.commit()

        return TeamSchema(uid=entity.uid, name=entity.name)

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

        return TeamSchema(uid=entity.uid, name=entity.name)

    def get_all(self) -> list[TeamSchema]:
        entity = Team.query.all()
        all_teams = []

        for team in entity:
            poi = TeamSchema(uid=team.uid, name=team.name)
            all_teams.append(poi)

        return all_teams
