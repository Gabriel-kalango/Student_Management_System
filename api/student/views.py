from flask_restx import abort,Resource
from ..model import StudentInfo,RegCourse,Course,BlockliskModel
from ..utils.utils import db
import random
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity,create_access_token,create_refresh_token
from ..schema import student_data,student_login,student_namespace,student_registeration,reg_course_namespace,reg_couse_model
from sqlalchemy import and_
from werkzeug.security import check_password_hash,generate_password_hash
#student registeration
@student_namespace.route("/reg")
class studentreg(Resource):
    @student_namespace.expect(student_registeration)
    @student_namespace.marshal_with(student_registeration)
    def post(self):
        data=student_namespace.payload
        if StudentInfo.query.filter( StudentInfo.email == data["email"]).first():
            abort(409, message="A Student with this email already exists.")

        a=str(random.randint(111111,999999))
        
        
        newstudent=StudentInfo(firstname=data.get("firstname").lower(),lastname=data.get("lastname").lower(),department=data.get("department").lower(),email=data.get("email"),matric_no=(str(a)+data.get("firstname")),password=data.get("lastname").upper())
        db.session.add(newstudent)
        db.session.commit()
        return newstudent,201
#course registeration    
@reg_course_namespace.route("/registercourse")   
class Coursereg(Resource):
    @jwt_required()
    @reg_course_namespace.expect(reg_couse_model)
    def post(self):
        data=reg_course_namespace.payload
        jwt=get_jwt()
        student_id=get_jwt_identity()
        course=Course.query.filter(Course.course_code==data.get("course_code")).first()
        if  jwt.get("is_admin"):
            abort(400,message="only students can register for a course")
        
        if not course:
            abort(400,message="this course code doesnt exist")
        if RegCourse.query.filter(and_(RegCourse.course_code==data.get("course_code"),RegCourse.student_id==student_id)).first():
            abort(400,message="you have already registered for this course")

        coursereg=RegCourse(course_name=course.course_name,course_code=course.course_code,teacher=course.teacher,student_id=student_id,course_id=course.id)
        db.session.add(coursereg)
        db.session.commit()
        return {"message":"course has been registered successfully"},201 
    

@student_namespace.route("/login")
class studentLogin(Resource):
    @student_namespace.expect(student_login)
    def post(self):
        """
            Generate access and Refresh Token
        """
        data=student_namespace.payload
        student=StudentInfo.query.filter(StudentInfo.matric_no==data["matric_no"]).first()
        if student.password==data["password"]:
            access_token=create_access_token(identity=student.id)
            refresh_token=create_refresh_token(identity=student.id)

            response={"access_token":access_token,"refresh_token":refresh_token}
            return response,200
        return {"message":"invalid credentials"}
        
@student_namespace.route('/refresh')
class Refresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        """
            Generate Refresh Token
        """
        jwt=get_jwt()
        if  jwt.get("is_admin"):
            abort(403,message="unauthorized user")

        id= get_jwt_identity()

        access_token = create_access_token(identity=id)

        return {"access_token": access_token},201

        
#get all students profile accessible by only admin
@student_namespace.route("/students")
class GetallStudents(Resource):
    @jwt_required()
    @student_namespace.marshal_with(student_data)
    def get(self):
        jwt=get_jwt()
        if not  jwt.get("is_admin"):
            abort(403,message="unauthorized user")

        students=StudentInfo.query.all()
        return students,200

 #get your (student) profile  
@student_namespace.route("/student")
class GetYourinfo(Resource):
    @jwt_required()
    @student_namespace.marshal_with(student_data)
    def get(self):
        jwt=get_jwt()
        if  jwt.get("is_admin"):
            abort(403,message="only the owner of this account can access this")
    
        id=get_jwt_identity()
        student=StudentInfo.query.filter(StudentInfo.id==id).first()
 
        return student,200
#student logout endpoint
@student_namespace.route("/logout")   
class Logout(Resource):
    @jwt_required()
    def post(self):
        jti=get_jwt().get("jti")
        j_ti=BlockliskModel(jwt=jti)
        db.session.add(j_ti)
        db.session.commit()
        return {"message":"user has been logged out "}
#delete student endpoint accessible by only admin
@student_namespace.route("/delete/<matric_no>")
class ExpellStudent(Resource):
    @jwt_required()
    
    def delete(self,matric_no):
        jwt=get_jwt()
        if not  jwt.get("is_admin"):
            abort(403,message="unauthorized user")
        student=StudentInfo.query.filter(StudentInfo.matric_no==matric_no).first
        db.session.delete(student)
        db.session.commit()
        return {"message":f"student with the {matric_no} has been rusticated"}
