from flask_restx import Namespace,fields
admin_namespace=Namespace("admin", description="operation on admin")
# creating schema for admin registeration
admin_registeration=admin_namespace.model(
    "admin_signup",{
    'id':fields.Integer(dump_only=True),
    'firstname':fields.String(required=True,description="An admin firstname"),
    'lastname':fields.String(required=True,description="An admin lastname"),

    'email':fields.String(required=True,description="an email"),
    'password':fields.String(required=True,description="An admin password")
}
)
# schema for admin signing in
admin_login=admin_namespace.model("login",{
    'email': fields.String(required=True, description="An email"),
    'password': fields.String(required=True, description="A password")
})

admin_reset_password=admin_namespace.model("reset",{
    'old_password': fields.String(required=True, description="old password"),
    'new_password': fields.String(required=True, description="new password")
    })