from datetime import datetime

from sqlalchemy.exc import IntegrityError

from backend.database import db_session
from backend.errors import ConflictError
from backend.models import Injury


class InjuryStorage:
    name = 'injuries'

    def add(
        self,
        name: str,
        description: str | None,
        start_date: datetime,
        end_date: datetime | None,
        player_id: int,
    ) -> Injury:
        entity = Injury(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            player_id=player_id,
        )
        try:
            db_session.add(entity)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return entity
