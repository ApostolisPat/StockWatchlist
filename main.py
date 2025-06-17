from jose import JWTError,jwt
from sqlalchemy import Column, Integer, String, DateTime, func, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "mysecretkey"  # keep it secret in prod
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app = FastAPI()

Base = declarative_base()

#Create an sqlite db
DATABASE_URL = "sqlite:///./test.db"
###First create the engine, which the session will use for the connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
###Then create a session. This handles all the CRUD operations, as well as rollback, and closing the connection at the end
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)
###Dependency to create a new session(object that does the CRUD Operations) for each request
def get_db():
    db = SessionLocal()
    try:
        #ChatGpt, why do we use yield?
        yield db
    finally:
        db.close()


#This is a model used in Database Queries. Like output/input models for communicate with the frontend, we use this model to connect to the database
class User(Base):
    __tablename__ = "users"
    
    id= Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
#Create input/output models
###For accepting user data in a request
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length = 6)
    
###For returning user data in a response
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    
    class Config:
        orm_mode = True
        
        
Base.metadata.create_all(bind=engine)

def hash_password(plain_pwd: str):
    pass
        
@app.post('/register')
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_check_username = db.query(User).filter(User.username == user_data.username).first()
    user_check_email = db.query(User).filter(User.email == user_data.email).first()
    if(user_check_username or user_check_email):
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    
    hashed_pwrd = hash_password(user_data.password)
    #Create the db model instance to send to the db
    new_user = User(username=user_data.username, email=user_data.email, hashed_password = hashed_pwrd)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload['sub']
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    #Find user in database from username we extracted from access token
    user = db.query(User).filter(User.username == username).first()
    return user

@app.get('/me', response_model=UserResponse)
def read_profile(current_user: User = Depends(get_current_user)):
    return current_user