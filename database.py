from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = "sqlite:///./watchlist.db"


engine = create_engine(url=DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

#Base for database models
Base=declarative_base()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()