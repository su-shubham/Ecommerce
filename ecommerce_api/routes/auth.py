from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
import json

security = HTTPBasic()

# Define a function to validate the JWT token
def validate_token(token: str):
    with open("./json/users.json", "r") as user_file:
        user_db = json.load(user_file)
    try:
        payload = jwt.decode(token, user_db["secret_key"], algorithms=["HS256"])
        username = payload["sub"]
        if username not in user_db["users"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Define a function to generate a JWT token for a given username and password
def generate_token(username: str, password: str):
    with open("./json/users.json", "r") as user_file:
        user_db = json.load(user_file)
    if username not in user_db["users"] or user_db["users"][username]["password"] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=user_db["access_token_expire_minutes"])
    access_token_payload = {"sub": username, "exp": datetime.utcnow() + access_token_expires}
    access_token = jwt.encode(access_token_payload, user_db["secret_key"], algorithm="HS256")
    return access_token

# Define a dependency function to validate the JWT token
def get_token(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    access_token = generate_token(username, password)
    validate_token(access_token)
    return access_token
