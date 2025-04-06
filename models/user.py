from sqlalchemy import Column, Integer, DateTime, func, String, Date
from sqlalchemy.ext.declarative import declarative_base
import string
import secrets


UserBase = declarative_base()

def generate_user_id(length=25):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

class User(UserBase):
    __tablename__ = 'user'
    
    id = Column(String, primary_key=True, default=generate_user_id)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False) 
    mobile_number = Column(String, nullable=False)
    plan = Column(String, nullable=False)
    period = Column(String, nullable=False)
    plan_start_date = Column(DateTime, default=func.now())
    plan_end_date = Column(DateTime, nullable=True)
    ai_credits =  Column(Integer, default=0)

    def __init__(self, create_dict, *arg, **kwargs):
        super(User, self).__init__(*arg, **kwargs)
        for key in create_dict:
            setattr(self, key, create_dict.get(key)) 
