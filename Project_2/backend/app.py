from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from .database import engine, get_db
from .models import Base, User, Message
from pydantic import BaseModel
from datetime import timedelta

app = FastAPI()

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    password: str

class MessageCreate(BaseModel):
    content: str
    receiver_id: int

@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User registered successfully"}

@app.post("/token/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/send_message/")
def send_message(message: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_message = Message(
        content=message.content, sender_id=current_user.id, receiver_id=message.receiver_id
    )
    db.add(new_message)
    db.commit()
    return {"msg": "Message sent successfully"}

@app.get("/messages/")
def get_messages(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    messages = (
        db.query(Message)
        .filter(Message.receiver_id == current_user.id)
        .order_by(Message.timestamp.desc())
        .all()
    )
    for message in messages:
        if not message.is_read:
            message.is_read = True
            db.add(message)
            db.commit()
    return messages
