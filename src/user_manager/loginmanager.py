# module containing essential functions required by flask-login extension!

from src import lm, mongo
from flask_login import UserMixin

lm.login_view = "user_manager.dlogin"


class Users(UserMixin):
    def __init__(self, email_id, *args, **kwargs):
        super().__init__()
        self.id = email_id


@lm.user_loader
def load_user(email_id):
    # check if user exists and load

    query_dict = {
        "email_id": email_id
    }

    db = mongo.db.UserBase
    user_exists = db.find(query_dict).count()

    if user_exists:
        return Users(email_id= email_id)
    else:
        return None
