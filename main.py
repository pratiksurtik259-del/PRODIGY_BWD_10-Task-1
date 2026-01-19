from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from typing import Dict

app = FastAPI(title="User CRUD API", version="1.0")

# -----------------------------
# In-memory storage (hashmap)
# -----------------------------
users_db: Dict[UUID, dict] = {}


# -----------------------------
# Pydantic Models
# -----------------------------
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    age: int = Field(..., gt=0, lt=150)


class User(UserCreate):
    id: UUID


# -----------------------------
# Create User
# -----------------------------
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    user_id = uuid4()

    new_user = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }

    users_db[user_id] = new_user
    return new_user


# -----------------------------
# Read All Users
# -----------------------------
@app.get("/users", response_model=list[User])
def get_users():
    return list(users_db.values())


# -----------------------------
# Read Single User
# -----------------------------
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: UUID):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return users_db[user_id]


# -----------------------------
# Update User
# -----------------------------
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, user: UserCreate):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    updated_user = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }

    users_db[user_id] = updated_user
    return updated_user


# -----------------------------
# Delete User
# -----------------------------
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    del users_db[user_id]
    return None
