# main.py
from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from kafka import KafkaProducer, KafkaConsumer
import json
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory user data
users_db = {
    "user1": {"username": "user1", "password": "password1"},
    "user2": {"username": "user2", "password": "password2"},
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class Message(BaseModel):
    sender: str
    receiver: str
    content: str
    timestamp: str
    unread: bool = True

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return token_data.username

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if user is None or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.websocket("/ws/{receiver}")
async def websocket_endpoint(websocket: WebSocket, receiver: str, user: str = Depends(get_current_user)):
    await websocket.accept()

    consumer = KafkaConsumer(
        receiver,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        group_id=user,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    try:
        for message in consumer:
            await websocket.send_json(message.value)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

@app.post("/send-message/")
async def send_message(message: Message, user: str = Depends(get_current_user)):
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda x: json.dumps(x).encode("utf-8")
    )
    producer.send(message.receiver, value=message.dict())
    producer.flush()
    return {"status": "message sent"}
