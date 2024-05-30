import bcrypt

def hashpw(password : str = None) -> str:
    """ Returns a hashed password typecasted to string."""

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def checkpw(password : str, hashed_password : str) -> bool:
    """ Returns True if the hashed_password was generated by the password"""

    return bcrypt.checkpw(password.encode(), hashed_password.encode())