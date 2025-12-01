from flask import Blueprint
import controllers.crystal_controller as controllers

crystals = Blueprint("crystals", __name__)

@crystals.route("/crystal", methods=["POST"])
def create_crystal():
    return controllers.create_crystal()

@crystals.route("/crystal/<crystal_id>", methods=["GET"])
def get_crystal(crystal_id):
    return controllers.get_crystal(crystal_id)

@crystals.route("/crystals/<rarity_level>", methods=["GET"])
def get_crystals_by_rarity(rarity_level):
    return controllers.get_crystals_by_rarity(rarity_level)

@crystals.route("/crystal/<crystal_id>", methods=["PUT"])
def update_crystal(crystal_id):
    return controllers.update_crystal(crystal_id)

@crystals.route("/crystal/<crystal_id>/delete", methods=["DELETE"])
def delete_crystal(crystal_id):
    return controllers.delete_crystal(crystal_id)
