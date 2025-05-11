from sqlalchemy.orm import Session
from db.models import User_Token as user_token_model
from schemas import user as user_schema
from schemas import auth as auth_schema


def store_refresh_token(db: Session, user_id: int,device_id:str, refresh_token_info:auth_schema.refresh_token_info):
    token_entry = user_token_model(user_id =user_id,
                                    refresh_token=refresh_token_info.refresh_token,
                                    device_id=device_id,
                                    expired_at=refresh_token_info.expired_at)
    exists = (
        db.query(user_token_model)
        .filter(user_token_model.user_id == token_entry.user_id,user_token_model.device_id == token_entry.device_id)
        .first()
    )
    if exists:
        exists.refresh_token = refresh_token_info.refresh_token
        exists.expired_at = refresh_token_info.expired_at
        db.commit()
        db.refresh(exists)
    else :
        db.add(token_entry)
        db.commit()
        db.refresh(token_entry)
    return token_entry