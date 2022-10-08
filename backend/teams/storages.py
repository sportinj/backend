from backend.teams.schemas import Team
from backend.errors import NotFoundError

class LocalStorage:
    def __init__(self):
        self.teams: dict[int, Team] = {}
        self.last_uid = 0

    def add(self, team: Team) -> Team :
        self.last_uid +=1
        team.uid = self.last_uid
        self.teams[self.last_uid] = team
        return team

    def get_teams(self) -> list[Team]:
        return list(self.teams.values())

    def get_team_by_id(self, uid:int) ->Team:
        if uid not in self.teams:
            raise NotFoundError('teams', uid)

        return self.teams[uid]


    def update(self, uid:int, team: Team) ->Team:
        if uid not in self.teams:
            raise NotFoundError('teams', uid)

        self.teams[uid] = team
        return team


    def delete(self, uid: int) -> None:
        if uid not in self.teams:
            raise NotFoundError('teams', uid)

        self.teams.pop(uid)
