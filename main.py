from fastapi import FastAPI
from .database import Base,engine
from .routers import users, watchlist


app = FastAPI()

#Create tables in db
Base.metadata.create_all(bind=engine)

#Add routers
app.include_router(users.router)
#app.include_router(watchlist.router)