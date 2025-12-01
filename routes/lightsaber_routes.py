from flask import Blueprint
import controllers.lightsaber_controller as controllers

lightsabers = Blueprint("lightsabers", __name__)

@lightsabers.route("/lightsaber", methods=["POST"])
def create_lightsaber():
    return controllers.create_lightsaber()

@lightsabers.route("/lightsaber/<saber_id>", methods=["GET"])
def get_lightsaber(saber_id):
    return controllers.get_lightsaber(saber_id)

@lightsabers.route("/lightsaber/owner/<owner_id>", methods=["GET"])
def get_lightsabers_by_owner(owner_id):
    return controllers.get_lightsabers_by_owner(owner_id)

@lightsabers.route("/lightsaber/<saber_id>", methods=["PUT"])
def update_lightsaber(saber_id):
    return controllers.update_lightsaber(saber_id)

@lightsabers.route("/lightsaber/<saber_id>/delete", methods=["DELETE"])
def delete_lightsaber(saber_id):
    return controllers.delete_lightsaber(saber_id)
