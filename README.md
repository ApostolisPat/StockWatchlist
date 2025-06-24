# StockWatchlist

A FastAPI application that allows users to register, log in, and manage a personalized stock watchlist. Stock data is fetched live using [yfinance](https://github.com/ranaroussi/yfinance).

## Features

- User registration and authentication (JWT-based)
- Add/remove stocks to/from your watchlist
- Fetch real-time stock data for your watchlist
- Secure endpoints (only authenticated users can manage their watchlist)
- SQLite database with SQLAlchemy ORM

## Requirements

- Python 3.10+
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [yfinance](https://github.com/ranaroussi/yfinance)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [python-jose](https://python-jose.readthedocs.io/en/latest/)

Install dependencies:
```sh
pip install fastapi uvicorn sqlalchemy yfinance bcrypt python-dotenv python-jose
```

## Setup

1. **Clone the repository** and navigate to the project folder.

2. **Create a `.env` file** in the project root with the following content:
    ```
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

3. **Run the application:**
    ```sh
    uvicorn main:app --reload
    ```

4. **Access the API docs:**  
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

## API Endpoints

### User

- `POST /users/register`  
  Register a new user.

- `POST /users/login`  
  Obtain a JWT token (use `username` and `password` as form fields).

- `GET /users/profile`  
  Get the current user's profile (requires authentication).

### Watchlist

- `POST /watchlist?symbol=SYMBOL`  
  Add a stock symbol to your watchlist.

- `GET /watchlist`  
  Get all stocks in your watchlist with live data.

- `DELETE /watchlist?symbol=SYMBOL`  
  Remove a stock symbol from your watchlist.

## Example Usage

1. **Register:**
    ```json
    POST /users/register
    {
      "username": "alice",
      "email": "alice@example.com",
      "password": "yourpassword"
    }
    ```

2. **Login:**
    ```json
    POST /users/login
    {
      "username": "alice",
      "password": "yourpassword"
    }
    ```
    Response:
    ```json
    {
      "access_token": "your.jwt.token",
      "token_type": "bearer"
    }
    ```

3. **Add to Watchlist:**
    ```
    POST /watchlist?symbol=AAPL
    Authorization: Bearer <access_token>
    ```

4. **Get Watchlist:**
    ```
    GET /watchlist
    Authorization: Bearer <access_token>
    ```

5. **Remove from Watchlist:**
    ```
    DELETE /watchlist?symbol=AAPL
    Authorization: Bearer <access_token>
    ```

## Project Structure

```
StockWatchlist/
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── auth.py
├── routers/
│   ├── users.py
│   └── watchlist.py
├── utils/
│   └── stock_validator.py
├── .env
└── README.md
```

## Notes

- All watchlist endpoints require authentication via JWT.
- Stock data is fetched live from Yahoo Finance using `yfinance`.
- Passwords are securely hashed using `bcrypt`.

---

**Enjoy managing your stock watchlist!**