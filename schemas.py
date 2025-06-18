from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=5)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    
    #UserResposne is used to show data from db, so use orm_mode to be compatible
    class Config:
        orm_mode = True
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class WatchlistCreate(BaseModel):
    id: int
    symbol: str
    created_at: datetime
    
    #To turn SQLAlchemy object to dictionary
    class Config:
        orm_mode = True
        
class WatchlistResponse(BaseModel):
    symbol: str