from ..utils.utils import db
class RegCourse(db.Model):
    __tablename__="Regcourse"
    id=db.Column(db.Integer,primary_key=True)
    course_code=db.Column(db.String,nullable=False)
    course_name=db.Column(db.String,nullable=False)
    teacher=db.Column(db.String,nullable=False)
    course_id=db.Column(db.Integer,db.ForeignKey("course.id"),nullable=False)
    student_id=db.Column(db.Integer,db.ForeignKey("students.id"),nullable=False)
    grade=db.Column(db.Integer,default=0)
    points=db.Column(db.Integer,default=0)
    


    def __repr__(self):
        return f"<user {self.course_name}>"