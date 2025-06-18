from typing import List
from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, auth, database

router = APIRouter(
    prefix="/watchlist",
    tags=["Watchlist"]
)

@router.post('')
def add_stock(symbol: str, db: Session = Depends(database.get_db), db_user: models.User = Depends(auth.get_current_user)):
    #Check if symbol already exists in their watchlist
    if db.query(models.Watchlist).filter((models.Watchlist.symbol == symbol) & (models.Watchlist.user_id == db_user.id)).first():
        raise HTTPException(status_code=409, detail="Symbol already exists")
    #Add new symbol in user's watchlist
    new_watchlist = models.Watchlist(
        user_id = db_user.id,
        symbol = symbol
    )
    
    #Add to session and commit
    db.add(new_watchlist)
    db.commit()
    db.refresh(new_watchlist)

    #Return success
    return {"message":f"{symbol} added to watchlist"}

@router.get('', response_model = List[schemas.WatchlistResponse])
def get_watchlist(db: Session = Depends(database.get_db), db_user: models.User = Depends(auth.get_current_user)):
    #Return all() the symbols
    return db.query(models.Watchlist).filter(models.Watchlist.user_id == db_user.id).all()