from backend.database import db_session
from backend.models import Team
from backend.teams.schemas import Team as TeamSchema
from backend.errors import NotFoundError


class LocalStorage:
    def __init__(self):
        self.teams: dict[int, TeamSchema] = {}
        self.last_uid = 0

    def add(self, team: TeamSchema) -> TeamSchema:
        self.last_uid += 1
        team.uid = self.last_uid
        self.teams[self.last_uid] = team
        return team

    def get_teams(self) -> list[TeamSchema]:
        return list(self.teams.values())

    def get_team_by_id(self, uid: int) -> TeamSchema:
        if uid not in self.teams:
            raise NotFoundError('teams', uid)

        return self.teams[uid]

    def update(self, uid: int, team: TeamSchema) -> TeamSchema:
        if uid not in self.teams:
            raise NotFoundError('teams', uid)

        return self.teams.pop(uid)

    def delete(self, uid: int) -> None:
        if uid not in self.teams:
            raise NotFoundError('teams', uid)

        self.teams.pop(uid)


class OnlineStorage(LocalStorage):
    def add(self, team: TeamSchema) -> TeamSchema:
        entity = Team(name=team.name)

        db_session.add(entity)
        db_session.commit()
        return TeamSchema(uid=entity.uid, name=entity.name)
