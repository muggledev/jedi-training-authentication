from flask import jsonify, request
from db import db
from datetime import datetime, timezone
from models.padawans import Padawans, padawan_schema, padawans_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, require_force_rank


@authenticate
@require_force_rank("Master")
def create_padawan():
    post_data = request.form if request.form else request.json

    padawan = Padawans.new_padawan_obj()
    populate_object(padawan, post_data)

    try:
        db.session.add(padawan)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create padawan"}), 400

    return jsonify({"message": "padawan created", "padawan": padawan_schema.dump(padawan)}), 201


@authenticate
def get_all_padawans():
    padawans = Padawans.query.all()
    return jsonify({"padawans": padawans_schema.dump(padawans)}), 200


@authenticate
def get_padawan(padawan_id):
    padawan = Padawans.query.get(padawan_id)
    if not padawan:
        return jsonify({"message": "padawan not found"}), 404

    return jsonify({"padawan": padawan_schema.dump(padawan)}), 200


@authenticate
def update_padawan(padawan_id):
    post_data = request.form if request.form else request.json
    padawan = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
    if not padawan:
        return jsonify({"message": "padawan not found"}), 404

    if request.user.force_rank not in ["Council", "Grand Master"] and request.user.user_id != padawan.master_id:
        return jsonify({"message": "not authorized"}), 403

    populate_object(padawan, post_data)
    db.session.commit()

    return jsonify({"message": "padawan updated", "padawan": padawan_schema.dump(padawan)}), 200


@authenticate
@require_force_rank("Council")
def delete_padawan(padawan_id):
    padawan = Padawans.query.get(padawan_id)
    if not padawan:
        return jsonify({"message": "padawan not found"}), 404

    db.session.delete(padawan)
    db.session.commit()

    return jsonify({"message": "padawan deleted"}), 200


@authenticate
@require_force_rank("Council")
def promote_padawan(padawan_id):
    padawan = Padawans.query.get(padawan_id)
    if not padawan:
        return jsonify({"message": "padawan not found"}), 404

    padawan.training_level = 999
    padawan.graduation_date = datetime.now(timezone.utc)

    db.session.commit()

    return jsonify({"message": "padawan promoted", "padawan": padawan_schema.dump(padawan)}), 200
