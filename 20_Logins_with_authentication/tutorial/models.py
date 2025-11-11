from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    func,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import register

DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    password = Column(String(100))
    date_created = Column(DateTime(timezone=True), default=func.now())
    date_modified = Column(DateTime(timezone=True), default=func.now())


Index('user_index', User.name, unique=True, mysql_length=255)
