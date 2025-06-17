import os
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from .database import get_db
from .models import User


load_dotenv()
SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def hash_password(plain_pwrd: str):
    hashed_pwrd = bcrypt.hashpw(plain_pwrd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(f"plain pwrd: {plain_pwrd}")
    print(f"hashed pwrd: {hashed_pwrd}")
    return hashed_pwrd
    
def verify_password(plain_pwrd: str, hashed_pwrd: str):
    return bcrypt.checkpw(plain_pwrd.encode('utf-8'), hashed_pwrd.encode('utf-8'))
    
    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    #update payload with expiry
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    #Create jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
    
def get_current_user(token: str = Depends(oauth2scheme), db: Session = Depends(get_db)) -> User:
    
    invalid_credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise invalid_credentials_exception
    except JWTError:
        raise invalid_credentials_exception
    
    user_db = db.query(User).filter(User.username == username).first()
    if user_db is None:
        raise invalid_credentials_exception
    return user_db
    