import functools
from flask import jsonify, request
from datetime import datetime, timezone
import uuid

from db import db
from models.auth_tokens import AuthTokens
from models.users import Users


FORCE_RANK_ORDER = {
    "Youngling": 1,
    "Padawan": 2,
    "Knight": 3,
    "Master": 4,
    "Council": 5,
    "Grand Master": 6
}


def validate_uuid4(uuid_string):
    try:
        uuid.UUID(uuid_string, version=4)
        return True
    except:
        return False


def validate_token():
    header = request.headers.get("Authorization")
    if not header:
        return False

    token = header.replace("Bearer", "").strip()

    if not validate_uuid4(token):
        return False

    token_uuid = uuid.UUID(token)
    existing_token = AuthTokens.query.filter_by(auth_token=token).first()
    if not existing_token:
        return False

    if existing_token.expiration_date > datetime.now(timezone.utc):
        return existing_token

    return False


def fail_response():
    return jsonify({"message": "authentication required"}), 401


def authenticate(func):
    """Simple decorator, only checks the token."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        auth_info = validate_token()
        return func(*args, **kwargs) if auth_info else fail_response()
    return wrapper


def authenticate_return_auth(func):
    """Decorator that injects auth_info into route args."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        auth_info = validate_token()
        kwargs["auth_info"] = auth_info
        return func(*args, **kwargs) if auth_info else fail_response()
    return wrapper


def require_force_rank(min_rank):
    if min_rank not in FORCE_RANK_ORDER:
        raise ValueError(f"Unknown Force rank: {min_rank}")

    required_value = FORCE_RANK_ORDER[min_rank]

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            auth = validate_token()
            if not auth:
                return fail_response()

            user = Users.query.get(auth.user_id)
            if not user:
                return jsonify({"message": "User not found"}), 401

            user_value = FORCE_RANK_ORDER.get(user.force_rank, 0)

            if user_value < required_value:
                return jsonify({
                    "message": "Insufficient rank",
                    "required_rank": min_rank,
                    "user_rank": user.force_rank
                }), 403

            return func(*args, **kwargs)

        return wrapper
    return decorator
