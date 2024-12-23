import jwt
import os
from decouple import config
from datetime import datetime
from jose import jwt, JWTError
from dotenv import load_dotenv
from dateutil import parser


load_dotenv()  # Load environment variables from .env file

JWT_SECRET = os.getenv("secret")
JWT_ALGORITHM = os.getenv("algorithm")

def token_response(token: str):
    return {
        "access_token": token
    }


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        exp_time = parser.isoparse(decoded_token["expires"])
        if exp_time >= datetime.utcnow():
            return decoded_token
        else:
            return None
    except JWTError as e:   
        print(f"Decoding error: {e}")  # Debug print
        return {}


