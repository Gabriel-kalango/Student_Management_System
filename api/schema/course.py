from flask_restx import Namespace,fields
course_namespace=Namespace("course",description="operation on course")
# creating schema for creating course
enum=['FIRST','SECOND']
couse_model=course_namespace.model("course",{
    'id':fields.Integer(dump_only=True),
    'course_code':fields.String(description=" the course code"),
    'course_name':fields.String(required=True,description=" the course name"),
    'teacher':fields.String( required=True ,description=" the  teacher offering the course"),
    'semester':fields.String(required=True,description="the current semester", enum=enum),
    
    

})