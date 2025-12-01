from flask import jsonify, request
from db import db
from models.temples import Temples, temple_schema, temples_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, require_force_rank


@authenticate
@require_force_rank("Grand Master")
def create_temple():
    data = request.get_json() or request.form
    temple = Temples()
    populate_object(temple, data)

    try:
        db.session.add(temple)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create temple"}), 400

    return jsonify({"message": "temple created", "temple": temple_schema.dump(temple)}), 201


@authenticate
@require_force_rank("Council")
def get_all_temples(auth_info):
    temples = Temples.query.all()
    return jsonify({"temples": temples_schema.dump(temples)}), 200


@authenticate
def get_temple(temple_id):
    temple = Temples.query.get(temple_id)
    if not temple:
        return jsonify({"message": "temple not found"}), 404

    return jsonify({"temple": temple_schema.dump(temple)}), 200


@authenticate
def get_all_temples():
    temples = Temples.query.all()
    return jsonify({"temples": temples_schema.dump(temples)}), 200


@authenticate
@require_force_rank("Grand Master")
def update_temple(temple_id):
    temple = Temples.query.get(temple_id)
    if not temple:
        return jsonify({"message": "temple not found"}), 404

    data = request.get_json() or request.form
    populate_object(temple, data)
    db.session.commit()

    return jsonify({"message": "temple updated", "temple": temple_schema.dump(temple)}), 200


@authenticate
@require_force_rank("Grand Master")
def delete_temple(temple_id):
    temple = Temples.query.get(temple_id)
    if not temple:
        return jsonify({"message": "temple not found"}), 404

    db.session.delete(temple)
    db.session.commit()

    return jsonify({"message": "temple deactivated"}), 200
