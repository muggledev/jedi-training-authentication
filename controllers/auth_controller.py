from flask import request, jsonify
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta, timezone
from db import db
from models.users import Users
from models.auth_tokens import AuthTokens, auth_token_schema
import uuid


FORCE_RANK_DURATION_MAP = {
    "Youngling": "TOKEN_EXPIRATION_YOUNGLING",
    "Padawan": "TOKEN_EXPIRATION_PADAWAN",
    "Knight": "TOKEN_EXPIRATION_KNIGHT",
    "Master": "TOKEN_EXPIRATION_MASTER",
    "Council": "TOKEN_EXPIRATION_COUNCIL",
    "Grand Master": "TOKEN_EXPIRATION_GRAND_MASTER"
}


def authenticate_user():
    data = request.get_json(silent=True) or request.form
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    user = Users.query.filter_by(email=email).first()

    print("Login attempt:", email)
    print("User found:", bool(user))

    if not user or not check_password_hash(user.password, password):
        print("Password match:", user and check_password_hash(user.password, password))
        return jsonify({"message": "invalid credentials"}), 401

    config_key = FORCE_RANK_DURATION_MAP.get(user.force_rank)
    duration_seconds = int(request.app.config.get(config_key, 3600))

    expiration = datetime.now(timezone.utc) + timedelta(seconds=duration_seconds)

    token = AuthTokens(
        auth_token=uuid.uuid4(),
        user_id=user.user_id,
        expiration_date=expiration
    )

    db.session.add(token)
    db.session.commit()

    return jsonify({
        "message": "login successful",
        "token": auth_token_schema.dump(token)
    }), 200

