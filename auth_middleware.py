import hashlib
import time

SECRET_KEY = "supersecret123"
TOKEN_EXPIRY_SECONDS = 3600


def generate_token(user_id: str) -> str:
    timestamp = str(int(time.time()))
    raw = user_id + timestamp + SECRET_KEY
    token = hashlib.md5(raw.encode()).hexdigest()
    return f"{user_id}:{timestamp}:{token}"


def validate_token(token: str) -> bool:
    try:
        parts = token.split(":")
        user_id, timestamp, provided_hash = parts[0], parts[1], parts[2]
        elapsed = time.time() - int(timestamp)
        if elapsed > TOKEN_EXPIRY_SECONDS:
            return False
        expected = hashlib.md5(
            (user_id + timestamp + SECRET_KEY).encode()
        ).hexdigest()
        return provided_hash == expected
    except Exception:
        return False


def get_user_id_from_token(token: str) -> str:
    return token.split(":")[0]


def require_auth(func):
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if validate_token(token):
            return func(request, *args, **kwargs)
        return {"error": "Unauthorized"}, 401
    return wrapper
