from functools import wraps
from flask import request, jsonify, current_app
from models.users import Users
from models.auth_tokens import AuthTokens
from datetime import datetime, timezone
import uuid


FORCE_RANK_ORDER = {
    "Youngling": 1,
    "Padawan": 2,
    "Knight": 3,
    "Master": 4,
    "Council": 5,
    "Grand Master": 6
}


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization")

        if not header:
            return jsonify({"message": "Missing token"}), 401

        token_str = header.replace("Bearer", "").strip()
        try:
            token_uuid = uuid.UUID(token_str)
        except ValueError:
            return jsonify({"message": "Invalid token format"}), 401

        auth = AuthTokens.query.filter_by(auth_token=token_uuid).first()
        if not auth:
            return jsonify({"message": "Invalid token"}), 401

        if auth.expiration_date < datetime.now(timezone.utc):
            return jsonify({"message": "Expired token"}), 401

        user = Users.query.get(auth.user_id)
        if not user or not user.is_active:
            return jsonify({"message": "User not found or inactive"}), 401

        request.user = user
        request.auth = auth

        return f(*args, **kwargs)
    return wrapper


def require_force_rank(min_rank):
    if min_rank not in FORCE_RANK_ORDER:
        raise ValueError(f"Unknown Force rank: {min_rank}")

    required_value = FORCE_RANK_ORDER[min_rank]

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not hasattr(request, "user"):
                return jsonify({"message": "Authentication required"}), 401

            user_rank = request.user.force_rank
            user_value = FORCE_RANK_ORDER.get(user_rank, 0)

            if user_value < required_value:
                return jsonify({
                    "message": "Insufficient rank",
                    "required_rank": min_rank,
                    "user_rank": user_rank
                }), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator


# -------------------------------------------------------------
# OPTIONAL: CHECK IF USER IS SELF OR HIGHER RANK
# For routes like: User can edit self OR Council+ can edit anyone
# -------------------------------------------------------------
def require_self_or_rank(min_rank):
    required_value = FORCE_RANK_ORDER[min_rank]

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not hasattr(request, "user"):
                return jsonify({"message": "Authentication required"}), 401

            user = request.user
            user_value = FORCE_RANK_ORDER.get(user.force_rank, 0)

            target_user_id = kwargs.get("user_id")  # works for /user/<user_id>

            # If editing own account → OK
            if target_user_id and str(user.user_id) == str(target_user_id):
                return f(*args, **kwargs)

            # Otherwise need required rank
            if user_value < required_value:
                return jsonify({"message": "Not authorized"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
