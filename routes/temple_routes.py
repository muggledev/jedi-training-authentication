from flask import Blueprint
import controllers.temple_controller as controllers

temples = Blueprint("temples", __name__)

@temples.route("/temple", methods=["POST"])
def create_temple():
    return controllers.create_temple()

@temples.route("/temples", methods=["GET"])
def get_all_temples_route():
    return controllers.get_all_temples()

@temples.route("/temple/<temple_id>", methods=["GET"])
def get_temple(temple_id):
    return controllers.get_temple(temple_id)

@temples.route("/temple/<temple_id>", methods=["PUT"])
def update_temple(temple_id):
    return controllers.update_temple(temple_id)

@temples.route("/temple/<temple_id>/delete", methods=["DELETE"])
def delete_temple(temple_id):
    return controllers.delete_temple(temple_id)
