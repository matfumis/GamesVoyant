import hashlib
from database import get_user_by_username, create_user

def hash_password(password: str) -> str:
    """
    A simple SHA-256 hash for demonstration purposes.
    (Alternatively, you could use bcrypt or passlib for more secure hashing.)
    """
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    """
    Checks if the username exists and if the provided password matches
    the stored password hash. Returns the user record if valid, or None otherwise.
    """
    user = get_user_by_username(username)
    if user:
        # Compare the stored hash with the hash of the provided password
        stored_hash = user["password_hash"]
        if stored_hash == hash_password(password):
            return user
    return None

def signup_user(username, password, name, surname, nationality, date_of_birth):
    """
    Create a new user if the username is not already taken.
    Returns (True, message) on success, (False, error_message) on failure.
    """
    existing_user = get_user_by_username(username)
    if existing_user is not None:
        return (False, "Username already taken.")
    
    # Hash the password
    hashed = hash_password(password)
    
    # Call the stored procedure to create the user
    create_user(username, hashed, name, surname, nationality, date_of_birth)
    
    return (True, "User created successfully.")
