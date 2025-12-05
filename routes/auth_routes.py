from flask import Blueprint
import controllers.auth_controller as controllers

auth = Blueprint("auth", __name__)

@auth.route("/user/auth", methods=["POST"])
def login_route():
    return controllers.create_auth_token()
