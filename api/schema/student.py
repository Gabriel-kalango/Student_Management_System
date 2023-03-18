from flask_restx import Namespace,fields
student_namespace=Namespace("student", description="operation on students")
# creating schema for student registeration
student_registeration=student_namespace.model(
    "signup",{
    'id':fields.Integer(dump_only=True),
    'firstname':fields.String(required=True,description="A student firstname"),
    'lastname':fields.String(required=True,description="A student lastname"),

    'email':fields.String(required=True,description="an email"),
    'matric_no':fields.String(description="a student Id"),
    "password":fields.String(description="a password"),
    'department':fields.String(required=True,description="A student department")
}
)

# student_reset_password=student_namespace.model("reset",{
#     'old_password': fields.String(required=True, description="old password"),
#     'new_password': fields.String(required=True, description="new password")
#     })
# creating schema for student info
from .regcourse import reg_couse_model
student_data=student_namespace.model(
    "studentinfo",{
    'id':fields.Integer(dump_only=True),
    'firstname':fields.String(required=True,description="A student firstname"),
    'lastname':fields.String(required=True,description="A student lastname"),
    'matric_no':fields.String(required=True,description="a student Id"),
    'email':fields.String(required=True,description="an email"),
    
    'department':fields.String(required=True,description="A student department"),
    'gpa':fields.Float(required=True,description="A student gpa"),
    'course_offered':fields.List(fields.Nested(reg_couse_model),description="course offered by the student ")
    }


)

# schema for student signing in
student_login=student_namespace.model("login_",{
    'matric_no': fields.String(required=True, description="student id"),
    'password': fields.String(required=True, description="A password")
})

studentview=student_namespace.model(
    "student",{
    'id':fields.Integer(dump_only=True),
    'firstname':fields.String(required=True,description="A student firstname"),
    'lastname':fields.String(required=True,description="A student lastname"),
    'matric_no':fields.String(required=True,description="a student Id"),
    'email':fields.String(required=True,description="an email"),
    
    'department':fields.String(required=True,description="A student department"),
    }


)