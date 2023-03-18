

import unittest
from .. import create_app
from ..utils.utils import db
from ..model  import Admin,StudentInfo,RegCourse,Course
from ..config.config import config_dict
from flask_jwt_extended import create_access_token

from werkzeug.security import generate_password_hash
import json



class UserTestCase(unittest.TestCase):
    
    def setUp(self):

        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()
        admin=Admin(firstname="watake",lastname="boruto",email="watake@gmail.com",password=generate_password_hash("nunez"))
        db.session.add(admin)
        db.session.commit()
    def tearDown(self):

        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None

   
    def test_admin_registration(self):

        data = {
            "firstname": "Test User",
            "lastname":"debug",
            "email": "testuser@gmail.com",
            "password": "password"
        }

        signup_response = self.client.post('/admin/registeration', json=data)

        user = Admin.query.filter(Admin.email=='testuser@gmail.com').first()

        assert user.firstname == "test user"

        assert signup_response.status_code == 201

    def test_user_login(self):
        data = {
            "email":"testuser@gmail.com",
            "password": "password"
        }
        login_response = self.client.post('/admin/login', json=data)

        assert login_response.status_code == 200

    def test_upload_grade(self):
        new_student=student=StudentInfo(firstname="test user",lastname="debuy",email="semo@gmail.com",password="DEBUY",matric_no="12345test user",department="aerospace")
        db.session.add(new_student)
        student=StudentInfo.query.filter(StudentInfo.firstname=="test user").first()
        course=Course(
                course_code="PYT101",
                course_name="advanced python",

                teacher="belleck",
                semester="FIRST"
        )
        db.session.add(course)
       
        token=create_access_token(identity="watake@gmail.com", additional_claims={"is_admin": True})
        coursee=Course.query.filter(Course.course_code=="PYT101").first()
        
        regisrerd_course=RegCourse(course_code=coursee.course_code,course_name=coursee.course_name,teacher=coursee.teacher,course_id=coursee.id,student_id=student.id)
        db.session.add(regisrerd_course)
        db.session.commit()
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Upload a valid grade for a student and assignment
        data={"grade":90}
        grade_response=self.client.put("/admin/student/1/1",json=data,headers=headers)
        assert grade_response.status_code == 200
          # Check that the uploaded grade is correct
        assert grade_response.json["message"] == "grade added successfully"
        
        # Upload an invalid grade (negative grade)
        data={"grade":-10,"points":""}
        grade_response=self.client.put("/admin/student/1/1",json=data,headers=headers)
        assert grade_response.status_code == 400

        # Upload an invalid grade (grade exceeds assignment max score)
        data={"grade":110,"points":""}
        grade_response=self.client.put("/admin/student/1/1",json=data,headers=headers)
        assert grade_response.status_code == 400

        # Upload a grade for a non-existent student
        data={"grade":50,"points":""}
        grade_response=self.client.put("/admin/student/999/1",json=data,headers=headers)
        assert grade_response.status_code == 404

        # Upload a grade for a non-existent assignment
        data={"grade":50,"points":""}
        grade_response=self.client.put("/admin/student/1/999",json=data,headers=headers)
        assert grade_response.status_code == 404

        # Upload a grade as a non-admin user
        studenttoken=create_access_token(identity="student@example.com")
        headers = {
            "Authorization": f"Bearer {studenttoken}"
        }
        data={"grade":90,"points":""}
        grade_response=self.client.put("/admin/student/1/1",json=data,headers=headers)
        assert grade_response.status_code == 403

    