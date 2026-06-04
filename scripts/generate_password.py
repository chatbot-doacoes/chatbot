import bcrypt


def generate_password(password: str):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt)
    print(password_hash.decode("utf-8"))

generate_password("123")