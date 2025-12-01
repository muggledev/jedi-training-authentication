from flask import Blueprint
import controllers.padawan_controller as controllers

padawans = Blueprint("padawans", __name__)

@padawans.route("/padawan", methods=["POST"])
def create_padawan():
    return controllers.create_padawan()

@padawans.route("/padawans", methods=["GET"])
def get_padawans():
    return controllers.get_all_padawans()

@padawans.route("/padawan/<padawan_id>", methods=["GET"])
def get_padawan(padawan_id):
    return controllers.get_padawan(padawan_id)

@padawans.route("/padawan/<padawan_id>", methods=["PUT"])
def update_padawan(padawan_id):
    return controllers.update_padawan(padawan_id)

@padawans.route("/padawan/<padawan_id>/delete", methods=["DELETE"])
def delete_padawan(padawan_id):
    return controllers.delete_padawan(padawan_id)

@padawans.route("/padawan/<padawan_id>/promote", methods=["PUT"])
def promote_padawan(padawan_id):
    return controllers.promote_padawan(padawan_id)
