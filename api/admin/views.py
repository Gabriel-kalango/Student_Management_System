from flask_restx import abort,Resource
from ..model import Admin,StudentInfo,RegCourse,BlockliskModel
from ..utils.utils import db
from flask_jwt_extended import get_jwt,get_jwt_identity,create_access_token,create_refresh_token,jwt_required
from ..schema import admin_namespace,admin_login,admin_registeration,student_namespace,student_data,reg_course_namespace,reg_couse_model,grade_model
from  werkzeug.security import generate_password_hash,check_password_hash
@admin_namespace.route("/registeration")
class adminRegisteration(Resource):
    @admin_namespace.expect(admin_registeration)
    def post(self):
        """
            admin registeration
        """
        data=admin_namespace.payload
        if Admin.query.filter(Admin.email==data["email"]).first():
            abort(400,message="admin with this email already exists")
        password_hash=generate_password_hash(data.get("password"))
        newadmin=Admin(firstname=data.get('firstname').lower(),lastname=data.get("lastname").lower(),email=data.get("email"), password=password_hash)
        db.session.add(newadmin)
        db.session.commit()
        return {"message":"admin created successfully"},201
    
@admin_namespace.route("/login")
class adminLogin(Resource):
    @admin_namespace.expect(admin_login)
    def post(self):
        """
            Generate access and Refresh Token
        """
        data=admin_namespace.payload
        admin=Admin.query.filter(Admin.email==data["email"]).first()
        if admin and check_password_hash(admin.password,data["password"]):
            access_token=create_access_token(identity=admin.email)
            refresh_token=create_refresh_token(identity=admin.email)

            response={"access_token":access_token,"refresh_token":refresh_token}
            return response,200
        
@admin_namespace.route('/refresh')
class Refresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        """
            Generate Refresh Token
        """
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(400,message="unauthorized user")

        email= get_jwt_identity()

        access_token = create_access_token(identity=email)

        return {'access_token': access_token}

@admin_namespace.route("/student/<int:student_id>/<int:course_id>")
class Studentfunctions(Resource):
    @jwt_required()
    @reg_course_namespace.expect(grade_model)
    def put(self,course_id,student_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(403,message="unauthorized user")

        data=reg_course_namespace.payload

        student=StudentInfo.query.get_or_404(student_id)
        student_course=RegCourse.query.filter(RegCourse.id==course_id).filter(RegCourse.student==student).first()
        if student_course is not None:

                if data.get("grade") >100 or data.get("grade")<0:
                    abort(400,message="grade should be between 0-100")
                student_course.grade=data.get("grade")
                if data.get("grade") >=70  and data.get("grade")<=100:
                    student_course.points=5
                elif data.get("grade") >=60  and data.get("grade")<=69:
                    student_course.points=4
                elif data.get("grade") >= 50 and data.get("grade")<=59:
                    student_course.points=3
                else:
                    student_course.points=0
                db.session.commit()
                return {"message":"grade added successfully"},200
        abort(404,message="course not found")    

@admin_namespace.route("/caculate-gp/<int:student_id>")
class Calculategp(Resource):
    @jwt_required()
    def put(self,student_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(403,message="unauthorized user")
        student=StudentInfo.query.get_or_404(student_id)
        sum_of_points=0
        credit_hour=0
        for course in student.course_offered.all():
            
            sum_of_points+=course.points
            credit_hour+=1
        if sum_of_points==0:
            return {"message":"advice to withdraw"}
        
        gpa=round((sum_of_points/credit_hour),2)

        student.gpa=gpa
        db.session.commit()
        return {"message":"gpa has been updated"},200
@admin_namespace.route("/logout")          
class Logout(Resource):
    @jwt_required()
    def post(self):
        jti=get_jwt().get("jti")
        j_ti=BlockliskModel(jwt=jti)
        db.session.add(j_ti)
        db.session.commit()
        return {"message":"user has been logged out "}
           




        
        

