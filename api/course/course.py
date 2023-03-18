from flask_restx import Resource,abort
from ..utils.utils import db
from ..schema import course_namespace,couse_model,student_namespace,studentview,student_data,reg_course_namespace,reg_couse_model,grade_model
from ..model import Course,RegCourse,StudentInfo
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity
import random


@course_namespace.route("/course")
class Coursee(Resource):
    @course_namespace.expect(couse_model)
    @course_namespace.marshal_with(couse_model)
    @jwt_required()
    def post(self):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(403,message="unauthorized user")

        data=course_namespace.payload
        if Course.query.filter(Course.course_name==data.get("course_name").lower()).first():
            abort(400,message="course already exists")
        a=random.randint(100,999)
        course_id=data.get("course_name")[:3]+str(a)
        newcourse=Course(course_name=data.get("course_name").lower(),course_code=course_id,teacher=data.get("teacher").lower(),semester=data.get("semester").upper())
        db.session.add(newcourse)
        db.session.commit()
    
        return newcourse,201
    @course_namespace.marshal_with(couse_model)
    def get(self):

        courses=Course.query.all()
        return courses,200
    
    @course_namespace.route("/<course_code>/students")
    class StudentsOfferingAcourse(Resource):
        @student_namespace.marshal_with(studentview)
        @jwt_required()
        def get(self,course_code):
            jwt=get_jwt()
            if not jwt.get("is_admin"):
                abort(403,message="unauthorized user")
            students = StudentInfo.query.join(RegCourse).filter(RegCourse.course_code == course_code).all()
            return students,200
            
    @course_namespace.route("/<course_code>/grades")
    class StudentsGradesinACourse(Resource):
        @reg_course_namespace.marshal_with(grade_model)
        @jwt_required()
        def get(self,course_code):
            jwt=get_jwt()
            if not jwt.get("is_admin"):
                abort(403,message="unauthorized user")
            students = RegCourse.query.filter(RegCourse.course_code == course_code).all()
            return students,200
            



 