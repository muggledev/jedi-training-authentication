from flask import jsonify, request
from db import db
from models.courses import Courses, course_schema, courses_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, require_force_rank


@authenticate
@require_force_rank("Master")
def create_course():
    data = request.get_json() or request.form

    course = Courses()
    populate_object(course, data)

    try:
        db.session.add(course)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create course"}), 400

    return jsonify({"message": "course created", "course": course_schema.dump(course)}), 201


@authenticate
def get_course(course_id):
    course = Courses.query.get(course_id)
    if not course:
        return jsonify({"message": "course not found"}), 404

    return jsonify({"course": course_schema.dump(course)}), 200


@authenticate
def get_courses_by_difficulty(difficulty_level):
    courses = Courses.query.filter_by(difficulty=difficulty_level).all()
    return jsonify({"courses": courses_schema.dump(courses)}), 200


@authenticate
def update_course(course_id):
    course = Courses.query.get(course_id)
    if not course:
        return jsonify({"message": "course not found"}), 404

    if request.user.user_id != course.instructor_id and request.user.force_rank not in ["Council", "Grand Master"]:
        return jsonify({"message": "not authorized"}), 403

    data = request.get_json() or request.form
    populate_object(course, data)
    db.session.commit()

    return jsonify({"message": "course updated", "course": course_schema.dump(course)}), 200


@authenticate
def delete_course(course_id):
    course = Courses.query.get(course_id)
    if not course:
        return jsonify({"message": "course not found"}), 404

    if request.user.user_id != course.instructor_id and request.user.force_rank not in ["Council", "Grand Master"]:
        return jsonify({"message": "not authorized"}), 403

    db.session.delete(course)
    db.session.commit()

    return jsonify({"message": "course deleted"}), 200
