from bot.database.session import SessionLocal
from bot.database.models.user_model import UserProfile
from bot.services.update_user import get_or_create_user

def get_top_ten_and_avg(discord_id: int):
    """
    returns top ten danger and avg danger of a user
    top ten danger is a list of message objects (I think)
    """
    db = SessionLocal()
    try:
        user = get_or_create_user(db, discord_id)

        top_messages = sorted(
            user.messages,
            key=lambda x: x.danger_score,
            reverse=True
        )
        danger_avg = user.danger_score

    finally:
        db.close()
    
    return top_messages, danger_avg



def get_ten_higher_danger():
    """
    returns the ten highest danger individuals
    """
    db = SessionLocal()
    try:
        users = (
            db.query(UserProfile)
            .order_by(UserProfile.danger_score.desc())
            .limit(10)
            .all()
        )

        if not users:
            return None
        
        return users
        
    finally:
        db.close()