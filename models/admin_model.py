from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    email: EmailStr
    password: str  # This will be hashed

class UserInDB(User):
    hashed_password: str