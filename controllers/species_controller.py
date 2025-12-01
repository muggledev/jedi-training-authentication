from flask import jsonify, request
from db import db
from models.species import Species, species_schema, species_list_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, require_force_rank


@authenticate
@require_force_rank("Master")
def create_species():
    data = request.get_json() or request.form
    species = Species()
    populate_object(species, data)

    try:
        db.session.add(species)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create species"}), 400

    return jsonify({"message": "species created", "species": species_schema.dump(species)}), 201


@authenticate
def get_species(species_id):
    species = Species.query.get(species_id)
    if not species:
        return jsonify({"message": "species not found"}), 404

    return jsonify({"species": species_schema.dump(species)}), 200


@authenticate
def get_all_species():
    species = Species.query.all()
    return jsonify({"species": species_list_schema.dump(species)}), 200


@authenticate
@require_force_rank("Master")
def update_species(species_id):
    species = Species.query.get(species_id)
    if not species:
        return jsonify({"message": "species not found"}), 404

    data = request.get_json() or request.form
    populate_object(species, data)
    db.session.commit()

    return jsonify({"message": "species updated", "species": species_schema.dump(species)}), 200


@authenticate
@require_force_rank("Master")
def delete_species(species_id):
    species = Species.query.get(species_id)
    if not species:
        return jsonify({"message": "species not found"}), 404

    db.session.delete(species)
    db.session.commit()

    return jsonify({"message": "species deleted"}), 200
