import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"


class Database:
    def __init__(self, name):
        class SelfBase(Base, DeclarativeBase):
            db = self

        os.makedirs("./var", exist_ok=True)
        url = f"sqlite:///./var/{name}.db"
        self.engine = create_engine(
            url, connect_args={"check_same_thread": False}
        )
        self.create_session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.Base = SelfBase

    def create_database(self):
        self.Base.metadata.create_all(self.engine)

    def drop_database(self):
        self.Base.metadata.drop_all(self.engine)
