from backend.db import Base
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.Users import Users


class Posts(Base):
    __tablename__ = 'posts'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    date_of_creation = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    users = relationship('Users')

if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable
    print(CreateTable(Posts.__table__))