import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()
DATA_FILE = Path("users.json")

# Ensure JSON file exists
if not DATA_FILE.exists():
    DATA_FILE.write_text("[]")

# Pydantic models
class User(BaseModel):
    id: int
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

# Helper functions
def read_users():
    with DATA_FILE.open("r") as f:
        return json.load(f)

def write_users(users):
    with DATA_FILE.open("w") as f:
        json.dump(users, f, indent=4)

def get_next_id(users):
    if not users:
        return 1
    return max(user["id"] for user in users) + 1

# CREATE
@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    users = read_users()
    new_user = {"id": get_next_id(users), "name": user.name, "email": user.email}
    users.append(new_user)
    write_users(users)
    return new_user

# READ ALL
@app.get("/users/", response_model=list[User])
def read_all_users():
    return read_users()

# READ ONE
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    users = read_users()
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# UPDATE
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    users = read_users()
    for user in users:
        if user["id"] == user_id:
            if user_update.name:
                user["name"] = user_update.name
            if user_update.email:
                user["email"] = user_update.email
            write_users(users)
            return user
    raise HTTPException(status_code=404, detail="User not found")

# DELETE
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    users = read_users()
    new_users = [user for user in users if user["id"] != user_id]
    if len(new_users) == len(users):
        raise HTTPException(status_code=404, detail="User not found")
    write_users(new_users)
    return {"message": "User deleted successfully"}