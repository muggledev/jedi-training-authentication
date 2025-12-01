from flask import Blueprint
import controllers.course_controller as controllers

courses = Blueprint("courses", __name__)

@courses.route("/course", methods=["POST"])
def create_course():
    return controllers.create_course()

@courses.route("/courses/<difficulty_level>", methods=["GET"])
def get_courses_by_difficulty(difficulty_level):
    return controllers.get_courses_by_difficulty(difficulty_level)

@courses.route("/course/<course_id>", methods=["GET"])
def get_course(course_id):
    return controllers.get_course(course_id)

@courses.route("/course/<course_id>", methods=["PUT"])
def update_course(course_id):
    return controllers.update_course(course_id)

@courses.route("/course/<course_id>/delete", methods=["DELETE"])
def delete_course(course_id):
    return controllers.delete_course(course_id)
