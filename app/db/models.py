from sqlalchemy import Column, Integer, String,DateTime,text,ForeignKey,UniqueConstraint,Boolean
from app.db.database import Base
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,autoincrement=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
    created_at =  Column(DateTime(timezone = True),server_default = text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone = True),onupdate=text('CURRENT_TIMESTAMP'))
    
class User_Token(Base):
    __tablename__='users_token'
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),index=True)
    device_id = Column(String,nullable=True)
    login_type = Column(String,server_default=text('local'))
    refresh_token = Column(String)
    expired_at = Column(DateTime(timezone=False))
    #use_yn = Column(Integer,server_default=text('1'))
    created_at =  Column(DateTime(timezone = True),server_default = text('CURRENT_TIMESTAMP'))
    
    #updated_at = Column(DateTime(timezone = True),onupdate=text('CURRENT_TIMESTAMP'))
    __table_args__ = (
        UniqueConstraint("user_id", "device_id","login_type", name="uq_user_device"),)
    
class Todo(Base):
    __tablename__='todo'
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),index=True)
    title =  Column(String)
    description = Column(String)
    todo_date =Column(DateTime(timezone=False))
    complete = Column(Integer)
    created_at =  Column(DateTime(timezone = True),server_default = text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone = True),onupdate=text('CURRENT_TIMESTAMP'))