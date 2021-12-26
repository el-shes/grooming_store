import jwt


def encode(user_id, role):
    key = "secret"
    encoded = jwt.encode({"id": user_id, "role": role.name}, key, algorithm="HS256")
    return encoded

def decode():
    pass

