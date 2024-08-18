from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from auth import create_access_token, verify_token
from kafka_consumer import get_unread_messages

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str

class Message(BaseModel):
    id: int
    content: str
    sentiment: str
    read: bool = False

fake_db = {
    "users": {
        "user1": {"username": "user1", "password": "password"},
    },
    "messages": []
}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_db["users"].get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/messages/unread")
async def get_unread_messages(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    unread_messages = get_unread_messages(username)
    return {"unread_messages": unread_messages}

@app.post("/messages")
async def post_message(message: Message, token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    # Save the message to the database
    message.id = len(fake_db["messages"]) + 1
    fake_db["messages"].append(message.dict())
    return {"message": "Message posted successfully"}
