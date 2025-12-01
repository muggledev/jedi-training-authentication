from flask import jsonify, request
from db import db
from models.crystals import Crystals, crystal_schema, crystals_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, require_force_rank


@authenticate
@require_force_rank("Master")
def create_crystal():
    data = request.get_json() or request.form

    crystal = Crystals()
    populate_object(crystal, data)

    try:
        db.session.add(crystal)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create crystal"}), 400

    return jsonify({"message": "crystal created", "crystal": crystal_schema.dump(crystal)}), 201


@authenticate
def get_crystal(crystal_id):
    crystal = Crystals.query.get(crystal_id)
    if not crystal:
        return jsonify({"message": "crystal not found"}), 404

    return jsonify({"crystal": crystal_schema.dump(crystal)}), 200


@authenticate
def get_crystals_by_rarity(rarity_level):
    crystals = Crystals.query.filter_by(rarity_level=rarity_level).all()
    return jsonify({"crystals": crystals_schema.dump(crystals)}), 200


@authenticate
@require_force_rank("Master")
def update_crystal(crystal_id):
    crystal = Crystals.query.get(crystal_id)
    if not crystal:
        return jsonify({"message": "crystal not found"}), 404

    data = request.get_json() or request.form
    populate_object(crystal, data)
    db.session.commit()

    return jsonify({"message": "crystal updated", "crystal": crystal_schema.dump(crystal)}), 200


@authenticate
@require_force_rank("Master")
def delete_crystal(crystal_id):
    crystal = Crystals.query.get(crystal_id)
    if not crystal:
        return jsonify({"message": "crystal not found"}), 404

    db.session.delete(crystal)
    db.session.commit()

    return jsonify({"message": "crystal deleted"}), 200
