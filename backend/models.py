from sqlalchemy import Column, Integer, String

from backend.database import Base, engine


class Player(Base):
    __tablename__ = 'players'

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


class Team(Base):
    __tablename__ = 'teams'
    uid = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
