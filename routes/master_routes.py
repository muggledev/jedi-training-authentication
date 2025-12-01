from flask import Blueprint
import controllers.master_controller as controllers

masters = Blueprint("masters", __name__)

@masters.route("/master", methods=["POST"])
def create_master():
    return controllers.create_master()

@masters.route("/masters", methods=["GET"])
def get_masters():
    return controllers.get_all_masters()

@masters.route("/master/<master_id>", methods=["GET"])
def get_master(master_id):
    return controllers.get_master(master_id)

@masters.route("/master/<master_id>", methods=["PUT"])
def update_master(master_id):
    return controllers.update_master(master_id)

@masters.route("/master/<master_id>/delete", methods=["DELETE"])
def delete_master(master_id):
    return controllers.delete_master(master_id)
