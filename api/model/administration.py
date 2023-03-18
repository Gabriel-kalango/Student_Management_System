from ..utils.utils import db
class Admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(25),nullable=False,unique=True)
    password=db.Column(db.Text(),nullable=False)
    
    def __repr__(self):
        return f"<user {self.firstname}>"