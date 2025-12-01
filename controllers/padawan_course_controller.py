from flask import jsonify, request
from db import db
from models.padawan_courses import PadawanCourses, enrollment_schema, enrollment_list_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, require_force_rank


@authenticate
@require_force_rank("Master")
def enroll_padawan():
    data = request.get_json() or request.form

    enrollment = PadawanCourses()
    populate_object(enrollment, data)

    try:
        db.session.add(enrollment)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to enroll padawan"}), 400

    return jsonify({"message": "padawan enrolled", "enrollment": enrollment_schema.dump(enrollment)}), 201


@authenticate
@require_force_rank("Master")
def get_all_enrollments(auth_info):
    enrollments = PadawanCourses.query.all()
    return jsonify({"enrollments": enrollment_list_schema.dump(enrollments)}), 200


@authenticate
def get_enrollment(padawan_id, course_id):
    enrollment = PadawanCourses.query.filter_by(
        padawan_id=padawan_id,
        course_id=course_id
    ).first()

    if not enrollment:
        return jsonify({"message": "enrollment not found"}), 404

    return jsonify({"enrollment": enrollment_schema.dump(enrollment)}), 200


@authenticate
@require_force_rank("Master")
def update_enrollment(padawan_id, course_id):
    enrollment = PadawanCourses.query.filter_by(
        padawan_id=padawan_id,
        course_id=course_id
    ).first()

    if not enrollment:
        return jsonify({"message": "enrollment not found"}), 404

    data = request.get_json() or request.form
    populate_object(enrollment, data)
    db.session.commit()

    return jsonify({"message": "enrollment updated", "enrollment": enrollment_schema.dump(enrollment)}), 200


@authenticate
@require_force_rank("Master")
def delete_enrollment(padawan_id, course_id):
    enrollment = PadawanCourses.query.filter_by(
        padawan_id=padawan_id,
        course_id=course_id
    ).first()

    if not enrollment:
        return jsonify({"message": "enrollment not found"}), 404

    db.session.delete(enrollment)
    db.session.commit()

    return jsonify({"message": "enrollment removed"}), 200
