import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class PadawanCourses(db.Model):
    __tablename__ = "PadawanCourses"

    padawan_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Padawans.padawan_id"), primary_key=True)
    course_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Courses.course_id"), primary_key=True)

    enrollment_date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completion_date = db.Column(db.DateTime())
    final_score = db.Column(db.Float())


class PadawanCoursesSchema(ma.Schema):
    padawan_id = ma.fields.UUID()
    course_id = ma.fields.UUID()
    enrollment_date = ma.fields.DateTime()
    completion_date = ma.fields.DateTime()
    final_score = ma.fields.Float()


enrollment_schema = PadawanCoursesSchema()
enrollment_list_schema = PadawanCoursesSchema(many=True)
