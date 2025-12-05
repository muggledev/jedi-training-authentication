from flask import jsonify, request
from db import db
from models.species import Species, species_schema, species_list_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, require_force_rank


@authenticate
@require_force_rank("Master")
def create_species():
    post_data = request.form if request.form else request.json

    species = Species.new_species_obj()
    populate_object(species, post_data)

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
    post_data = request.form if request.form else request.json
    species = db.session.query(Species).filter(Species.species_id == species_id).first()
    if not species:
        return jsonify({"message": "species not found"}), 404

    populate_object(species, post_data)
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
