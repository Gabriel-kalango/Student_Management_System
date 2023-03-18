import unittest
from .. import create_app
from ..utils.utils import db
from ..model  import StudentInfo,Course,RegCourse
from ..config.config import config_dict
from flask_jwt_extended import create_access_token

from werkzeug.security import generate_password_hash



class UserTestCase(unittest.TestCase):
    
    def setUp(self):

        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()
        student=StudentInfo(firstname="test user",lastname="debuy",email="semo@gmail.com",password="DEBUY",matric_no="12345test user",department="aerospace")
        db.session.add(student)
        db.session.commit()

    def tearDown(self):

        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None
    
    def test_student_registration(self):

        data = {
            "firstname": "Test User",
            "lastname":"debug",
            "email": "testuser1@gmail.com",
            "department":"aerospace"
        }
        
        signup_response = self.client.post('/student/reg', json=data)

        user = StudentInfo.query.filter(StudentInfo.email=='testuser1@gmail.com').first()

        assert user.firstname == "test user"

        assert signup_response.status_code == 201

    def test_student_login(self):
        user = StudentInfo.query.filter(StudentInfo.email=='semo@gmail.com').first()
        data={
            "matric_no":user.matric_no,
            "password":"DEBUY"
        }
        login_response=self.client.post("/student/login",json=data)
        assert login_response.status_code == 200

    def test_student_course_reg(self):
        courses = Course(course_code='test_course', course_name='Test Course', teacher='Test Teacher', semester='FIRST')
        db.session.add(courses)
        db.session.commit()
        
        
        
        student = StudentInfo.query.filter(StudentInfo.email=='semo@gmail.com').first()
        course = Course.query.filter(Course.course_code=='test_course').first()
        # Log in as the test student
        data={
            "matric_no": student.matric_no,
            "password": "DEBUY"
        }
        login_response=self.client.post("/student/login",json=data)
        assert login_response.status_code == 200
        access_token = create_access_token(identity=student.id)
        
        # Attempt to register for the test course
        data = {"course_code": "test_course"}
        headers = {"Authorization": f"Bearer {access_token}"}
        reg_response=self.client.post("/RegCourse/registercourse",json=data,headers=headers)
        
        # Check that the registration was successful
        assert reg_response.status_code == 201
        registered_course=RegCourse.query.filter(RegCourse.student_id==student.id,RegCourse.course_id==course.id).first()
        assert registered_course is not None
        # Attempt to register for a non-existent course
        data = {"course_code": "non_existent_course"}
        reg_response=self.client.post("/RegCourse/registercourse",json=data,headers=headers)
        
        # Check that the registration was unsuccessful
        assert reg_response.status_code == 400
        assert RegCourse.query.filter_by(student_id=student.id, course_id=course.id).first() 
    
   