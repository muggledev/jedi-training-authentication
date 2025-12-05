import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class Courses(db.Model):
    __tablename__ = "Courses"

    course_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    instructor_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Masters.master_id"))

    course_name = db.Column(db.String(), unique=True, nullable=False)
    difficulty = db.Column(db.String(), nullable=False)
    duration_weeks = db.Column(db.Integer(), nullable=False)
    max_students = db.Column(db.Integer(), nullable=False)

    def __init__(self, instructor_id, course_name, difficulty, duration_weeks, max_students):
        self.instructor_id = instructor_id
        self.course_name = course_name
        self.difficulty = difficulty
        self.duration_weeks = duration_weeks
        self.max_students = max_students

    def new_course_obj():
        return Courses('', '', '', 0, 0)


class CoursesSchema(ma.Schema):
    class Meta:
        fields = ['course_id', 'instructor_id', 'course_name', 'difficulty', 'duration_weeks', 'max_students']
    course_id = ma.fields.UUID()
    instructor_id = ma.fields.UUID()
    course_name = ma.fields.Str()
    difficulty = ma.fields.Str()
    duration_weeks = ma.fields.Int()
    max_students = ma.fields.Int()


course_schema = CoursesSchema()
courses_schema = CoursesSchema(many=True)
