from sqlalchemy import create_engine, String, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


class Player(Base):
    __tablename__ = 'player_ulitov'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    nickname = Column(String)
    discipline = Column(String)
    team = Column(String)
