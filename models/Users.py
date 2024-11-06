from backend.db import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)

    posts = relationship('Posts')


if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable
    print(CreateTable(Users.__table__))