import hashlib
from database import get_user_by_username, create_user

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    user = get_user_by_username(username)
    if user:
        stored_hash = user["password_hash"]
        if stored_hash == hash_password(password):
            return user
    return None

def signup_user(username, password, name, surname, nationality, date_of_birth):
    existing_user = get_user_by_username(username)
    if existing_user is not None:
        return (False, "Username already taken.")
    
    hashed = hash_password(password)
    
    create_user(username, hashed, name, surname, nationality, date_of_birth)
    
    return (True, "User created successfully.")
