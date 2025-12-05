from flask import jsonify, request
from flask_bcrypt import generate_password_hash
from db import db
from models.users import Users, user_schema, users_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, require_force_rank


def create_user():
    post_data = request.form if request.form else request.json

    new_user = Users.new_user_obj()
    populate_object(new_user, post_data)

    if not new_user.password:
        return jsonify({"message": "password required"}), 400

    new_user.password = generate_password_hash(new_user.password).decode("utf8")

    if not new_user.force_rank:
        new_user.force_rank = "Youngling"

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create user"}), 400

    return jsonify({"message": "user created", "user": user_schema.dump(new_user)}), 201


@require_force_rank("Council")
@authenticate
def get_all_users():
    users = Users.query.all()
    return jsonify({"users": users_schema.dump(users)}), 200


@authenticate
def get_own_profile():
    return jsonify({"user": user_schema.dump(request.user)}), 200


@authenticate
@require_force_rank("Council")
def get_user_by_id(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "user not found"}), 404
    return jsonify({"user": user_schema.dump(user)}), 200


@authenticate
def update_user(user_id):
    post_data = request.form if request.form else request.json
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        return jsonify({"message": "user not found"}), 404

    if str(request.user.user_id) != user_id and request.user.force_rank not in ["Council", "Grand Master"]:
        return jsonify({"message": "not authorized"}), 403

    if "password" in post_data:
        post_data["password"] = generate_password_hash(post_data["password"]).decode("utf8")

    populate_object(user, post_data)
    db.session.commit()

    return jsonify({"message": "user updated", "user": user_schema.dump(user)}), 200


@authenticate
@require_force_rank("Grand Master")
def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "user not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "user deleted"}), 200
