from flask import jsonify, request
from db import db
from models.masters import Masters, master_schema, masters_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, require_force_rank


@authenticate
@require_force_rank("Council")
def create_master():
    post_data = request.form if request.form else request.json

    master = Masters.new_master_obj()
    populate_object(master, post_data)

    try:
        db.session.add(master)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to promote user to master"}), 400

    return jsonify({"message": "master created", "master": master_schema.dump(master)}), 201


@authenticate
def get_all_masters():
    masters = Masters.query.all()
    return jsonify({"masters": masters_schema.dump(masters)}), 200


@authenticate
def get_master(master_id):
    master = Masters.query.get(master_id)
    if not master:
        return jsonify({"message": "master not found"}), 404

    return jsonify({"master": master_schema.dump(master)}), 200


@authenticate
def update_master(master_id):
    post_data = request.form if request.form else request.json
    master = db.session.query(Masters).filter(Masters.master_id == master_id).first()
    if not master:
        return jsonify({"message": "master not found"}), 404

    if str(request.user.user_id) != str(master.user_id) and request.user.force_rank not in ["Council", "Grand Master"]:
        return jsonify({"message": "not authorized"}), 403

    populate_object(master, post_data)
    db.session.commit()

    return jsonify({"message": "master updated", "master": master_schema.dump(master)}), 200


@authenticate
@require_force_rank("Grand Master")
def delete_master(master_id):
    master = Masters.query.get(master_id)
    if not master:
        return jsonify({"message": "master not found"}), 404

    db.session.delete(master)
    db.session.commit()

    return jsonify({"message": "master removed"}), 200
