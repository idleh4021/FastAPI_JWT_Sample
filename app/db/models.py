from sqlalchemy import Column, Integer, String,DateTime,text,ForeignKey,UniqueConstraint
from db.database import Base

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
    
    id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),primary_key=True)
    device_id = Column(String, primary_key=True)
    refresh_token = Column(String)
    expired_at = Column(DateTime(timezone=False))
    #use_yn = Column(Integer,server_default=text('1'))
    created_at =  Column(DateTime(timezone = True),server_default = text('CURRENT_TIMESTAMP'))
    #updated_at = Column(DateTime(timezone = True),onupdate=text('CURRENT_TIMESTAMP'))
    __table_args__ = (
        UniqueConstraint("id", "device_id", name="uq_user_device"),)