from ..utils.utils import db
class StudentInfo(db.Model):
    __tablename__="students"
    id=db.Column(db.Integer,primary_key=True)
    matric_no=db.Column(db.String(50),unique=True)
    firstname=db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(25),nullable=False,unique=True)
    password=db.Column(db.Text(),nullable=False)
    department=db.Column(db.String(50),nullable=False)
    gpa=db.Column(db.Float,default=0.00)
    course_offered=db.relationship('RegCourse',backref='student',cascade="all, delete",lazy='dynamic')


    

    def __repr__(self):
        return f"<user {self.student_id}>"