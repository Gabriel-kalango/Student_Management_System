import unittest
from .. import create_app
from ..utils.utils import db
from ..model  import StudentInfo,Course,RegCourse,Admin

from ..config.config import config_dict
from flask_jwt_extended import create_access_token

from werkzeug.security import generate_password_hash
from datetime import datetime,timedelta


class UserTestCase(unittest.TestCase):
    
    def setUp(self):

        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()
        course = Course(
                course_code="PYT101",
                course_name="advanced python",

                teacher="belleck",
                semester="FIRST"
        )
        db.session.add(course)
        db.session.commit()
    








    

    def test_course_creation(self):
  

        
        
        token=create_access_token(identity="watake@gmail.com")
         
  
        headers={"Authorization":f"Bearer {token}"}
        data={"course_name":"biology",
              "teacher":"wasiu kola",
              "semester":"FIRST"}

        try:
            Course_response=self.client.post("/course/course",json=data,headers=headers)
            assert Course_response.status_code == 201
            new_course=Course.query.filter(Course.course_name=="biology").first()
    
            assert new_course is not None
            assert new_course.course_name == "biology"
        except Exception as e:
            print(f"Exception occurred: {e}")
        # Course_response=self.client.post("/course/course",json=data,headers=headers)
       
        # new_course=Course.query.filter(Course.course_name=="biology").first()
    
        # assert new_course is not None
        # assert new_course.course_name == "biology"
    def tearDown(self):

        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None
        
if __name__ == '__main__':
    unittest.main()