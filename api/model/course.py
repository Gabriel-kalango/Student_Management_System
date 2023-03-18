from ..utils.utils import db
from enum import Enum
class Semester(Enum):
    FIRST="first_semester"
    SECOND="second_semester"
class Course(db.Model):
    __tablename__="course"
    id=db.Column(db.Integer,primary_key=True)
    course_code=db.Column(db.String,unique=True,nullable=False)
    course_name=db.Column(db.String,unique=True,nullable=False)
    teacher=db.Column(db.String,unique=True,nullable=False)
    semester=db.Column(db.Enum(Semester),nullable=False)
    
    


    def __repr__(self):
        return f"< {self.course_name}>"