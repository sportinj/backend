from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base, engine


class Player(Base):
    __tablename__ = 'players'

    uid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.uid'), nullable=False)


class Team(Base):
    __tablename__ = 'teams'
    uid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    players = relationship('Player')


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
