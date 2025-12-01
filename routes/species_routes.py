from flask import Blueprint
import controllers.species_controller as controllers

species = Blueprint("species", __name__)

@species.route("/species", methods=["POST"])
def create_species():
    return controllers.create_species()

@species.route("/species", methods=["GET"])
def get_all_species():
    return controllers.get_all_species()

@species.route("/species/<species_id>", methods=["GET"])
def get_species(species_id):
    return controllers.get_species(species_id)

@species.route("/species/<species_id>", methods=["PUT"])
def update_species(species_id):
    return controllers.update_species(species_id)

@species.route("/species/<species_id>/delete", methods=["DELETE"])
def delete_species(species_id):
    return controllers.delete_species(species_id)
