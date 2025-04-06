"""from jose import jwt

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
token = jwt.encode({"user_id": "alice"}, SECRET_KEY, algorithm=ALGORITHM)
print(token)
"""

from sqlalchemy import Column, Integer, DateTime, func, String, Date
from sqlalchemy.ext.declarative import declarative_base
import string
import secrets


from jose import jwt

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
token = jwt.encode({"user_id": "XdfVm1rBQJsNxrvGSHeGBETXd"}, SECRET_KEY, algorithm=ALGORITHM)
print(token)


"""def generate_user_id(length=25):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

token = generate_user_id()
"""