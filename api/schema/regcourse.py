from flask_restx import Namespace,fields
reg_course_namespace=Namespace("RegCourse",description="operation on course registeration")
# creating schema for registering course

reg_couse_model=reg_course_namespace.model("Course",{
    'id':fields.Integer(dump_only=True),
    'course_code':fields.String(required=True,description=" the course code"),
    'course_name':fields.String(description=" the course name"),
    'teacher':fields.String( description=" the  teacher offering the course"),
    'grade':fields.Integer(description="grade in the course"),
    'points':fields.Integer(description="point in the course")
    

})
grade_model=reg_course_namespace.model("grade",{
    'grade':fields.Integer(description="grade in the course")
    

})
