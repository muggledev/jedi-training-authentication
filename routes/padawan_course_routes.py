from flask import Blueprint
import controllers.padawan_course_controller as controllers

enrollments = Blueprint("enrollments", __name__)

@enrollments.route("/enrollment", methods=["POST"])
def enroll_padawan():
    return controllers.enroll_padawan()

@enrollments.route("/enrollments", methods=["GET"])
def get_all_enrollments():
    return controllers.get_all_enrollments()

@enrollments.route("/enrollment/<padawan_id>/<course_id>", methods=["GET"])
def get_enrollment(padawan_id, course_id):
    return controllers.get_enrollment(padawan_id, course_id)

@enrollments.route("/enrollment/<padawan_id>/<course_id>", methods=["PUT"])
def update_enrollment(padawan_id, course_id):
    return controllers.update_enrollment(padawan_id, course_id)

@enrollments.route("/enrollment/<padawan_id>/<course_id>/delete", methods=["DELETE"])
def delete_enrollment(padawan_id, course_id):
    return controllers.delete_enrollment(padawan_id, course_id)
