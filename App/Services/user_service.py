from ..Models.models import User, db

def create_user(user_info):
    user = User(**user_info)
    db.session.add(user)
    db.session.commit()
