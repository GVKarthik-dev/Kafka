from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, auth, database

app = FastAPI()

@app.post("/register/")
def register_user(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token/")
def login_for_access_token(db: Session = Depends(database.SessionLocal), form_data: schemas.UserCreate = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/messages/")
def read_messages(skip: int = 0, limit: int = 10, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.SessionLocal)):
    messages = db.query(models.Message).filter(models.Message.user_id == current_user.id).offset(skip).limit(limit).all()
    return messages

@app.post("/messages/")
def create_message(message: schemas.MessageCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.SessionLocal)):
    db_message = models.Message(**message.dict(), user_id=current_user.id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
