from datetime import datetime
from typing import List, Optional
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
    

class HistoricalDate(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float    
    volume: int
    dividends: float
    stock_splits: float

class StockData(BaseModel):
    symbol: str
    name: str
    price: float
    currency: str
    change_percent: float
    open: float
    high: float
    low: float
    volume: int
    market_cap: Optional[float]
    history: Optional[List[HistoricalDate]]