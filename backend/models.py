from sqlalchemy import Column, Integer

from backend.database import Base, engine


class Team(Base):
    __tablename__ = 'teams'
    uid = Column(Integer, primary_key=True)


if __name__ == '__main__':
    print('Try to create')
    Base.metadata.create_all(bind=engine)
    print('Created')
