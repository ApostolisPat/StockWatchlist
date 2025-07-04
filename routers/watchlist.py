from typing import List, Annotated
from fastapi import APIRouter, Depends,HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, auth, database
from ..utils.stock_validator import is_valid_stock_symbol
import yfinance as yf

router = APIRouter(
    prefix="/watchlist",
    tags=["Watchlist"]
)

@router.post('')
def add_stock(symbol: Annotated[str, Query(min_length=2, max_length=10)], db: Session = Depends(database.get_db), db_user: models.User = Depends(auth.get_current_user)):
    #Check if symbol exists in yahoo
    if not is_valid_stock_symbol(symbol):
        raise HTTPException(status_code=404, detail=f"Stock with symbol {symbol} does not exist in yahoo database")
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

@router.get('', response_model = List[schemas.StockData])
def get_watchlist(db: Session = Depends(database.get_db), db_user: models.User = Depends(auth.get_current_user)):
    #Return all() the symbols
    watchlist_items = db.query(models.Watchlist).filter(models.Watchlist.user_id == db_user.id).all()
    stock_data = []
    stock_historic_data = []
    for item in watchlist_items:
        ticker = yf.Ticker(item.symbol)
        info = ticker.info

        #Save historic data
        history = ticker.history(period="3d")
        print(history)
        for index, row in history.iterrows():
            stock_historic_data.append({
                "date": index.strftime("%m-%d-%Y"),
                "open": row['Open'],
                "high": row['High'],
                "low": row['Low'],
                "close": row['Close'],
                "volume": row['Volume'],
                "dividends": row.get('Dividends', 0),
                "stock_splits": row.get('Stock Splits', 0)
            })

        
        if not info or 'regularMarketPrice' not in info:
            continue

        stock_data.append({
            "symbol" : item.symbol,
            "name": info.get("shortName", "N/A"),
            "price": info.get('regularMarketPrice', 0),
            "currency": info.get("currency", "EUR"),
            "change_percent": info.get('regularMarketChangePercent','N/A'),
            "open": info.get('regularMarketOpen','N/A'),
            "high": info.get('regularMarketDayHigh','N/A'),
            "low": info.get('regularMarketDayLow','N/A'),
            "volume": info.get('regularMarketVolume','N/A'),
            "market_cap": info.get('marketCap','N/A'),
            "history": stock_historic_data
        })
        
    return stock_data

@router.delete('')
def remove_symbol(symbol:str, db: Session = Depends(database.get_db), db_user: models.User = Depends(auth.get_current_user)):
    symbol_db = db.query(models.Watchlist).filter((models.Watchlist.user_id == db_user.id) & (models.Watchlist.symbol == symbol)).first()
    if symbol_db is None:
        raise HTTPException(status_code=404, detail="Stock symbol not found")
    db.delete(symbol_db)
    db.commit()
    return {"message": f"{symbol} removed from watchlist"}