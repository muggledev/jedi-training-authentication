from flask import jsonify, request
from db import db
from models.lightsabers import Lightsabers, lightsaber_schema, lightsabers_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, require_force_rank


@authenticate
@require_force_rank("Padawan")
def create_lightsaber():
    data = request.get_json() or request.form

    saber = Lightsabers()
    populate_object(saber, data)

    try:
        db.session.add(saber)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create lightsaber"}), 400

    return jsonify({"message": "lightsaber created", "lightsaber": lightsaber_schema.dump(saber)}), 201


@authenticate
def get_lightsaber(saber_id):
    saber = Lightsabers.query.get(saber_id)
    if not saber:
        return jsonify({"message": "lightsaber not found"}), 404

    return jsonify({"lightsaber": lightsaber_schema.dump(saber)}), 200


@authenticate
def get_lightsabers_by_owner(owner_id):
    sabers = Lightsabers.query.filter_by(owner_id=owner_id).all()
    return jsonify({"lightsabers": lightsabers_schema.dump(sabers)}), 200


@authenticate
def update_lightsaber(saber_id):
    saber = Lightsabers.query.get(saber_id)
    if not saber:
        return jsonify({"message": "lightsaber not found"}), 404

    if request.user.force_rank not in ["Council", "Grand Master"] and request.user.user_id != saber.owner_id:
        return jsonify({"message": "not authorized"}), 403

    data = request.get_json() or request.form
    populate_object(saber, data)
    db.session.commit()

    return jsonify({"message": "lightsaber updated", "lightsaber": lightsaber_schema.dump(saber)}), 200


@authenticate
def delete_lightsaber(saber_id):
    saber = Lightsabers.query.get(saber_id)
    if not saber:
        return jsonify({"message": "lightsaber not found"}), 404

    if request.user.force_rank not in ["Council", "Grand Master"] and request.user.user_id != saber.owner_id:
        return jsonify({"message": "not authorized"}), 403

    db.session.delete(saber)
    db.session.commit()

    return jsonify({"message": "lightsaber deleted"}), 200
