from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, auth, database

router = APIRouter(prefix="/users", tags=["Users"])

@router.post('/register', response_model = schemas.UserResponse)
def register(new_user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    #Check if user exists
    if db.query(models.User).filter(models.User.username == new_user.username).first():
        raise HTTPException(status_code = 400, detail = f"User with username {new_user.username} already exists.")
    if db.query(models.User).filter(models.User.email == new_user.email).first():
        raise HTTPException(status_code = 400, detail = f"User with email {new_user.email} already exists.")
    
    #Hash password
    hashed_pwrd = auth.hash_password(new_user.password)
    
    #Create database model
    new_user = models.User(
        username = new_user.username,
        email = new_user.email,
        password = hashed_pwrd
    )
    
    #CRUD Operation
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not db_user or not auth.verify_password(form_data.password, str(db_user.password)):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    access_token = auth.create_access_token({"sub": str(db_user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/all', response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users
    


@router.get("/profile", response_model=schemas.UserResponse)
def get_user_profile(current_user: models.User = Depends(auth.get_current_user)):
    return current_user