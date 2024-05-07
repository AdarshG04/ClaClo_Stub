from fastapi import APIRouter, HTTPException
from models.admin_model import User, UserInDB
from config.database import collection_name
from bson import ObjectId
from utilities.security import hash_password, create_access_token, verify_password


auth_router = APIRouter()

# User Registration

@auth_router.post("/signup")
async def signup(user: User):
    user_in_db = collection_name.find_one({"email": user.email})
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    collection_name.insert_one({"email": user.email, "hashed_password": hashed_password})
    return {"message": "User created successfully."}

# User Login

@auth_router.post("/login")
async def login(user: User):
    user_in_db = collection_name.find_one({"email": user.email})
    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, user_in_db["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}