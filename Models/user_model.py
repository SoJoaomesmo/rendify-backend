from flask_sqlalchemy import SQLAlchemy
import werkzeug.security

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(128), nullable=True)
    
    def check_password(self, password_to_check:str): #  werkzeug.security.check_password_hash(self.password_hash, password_to_check)]
        if(password_to_check is None):
            return {"Message":"Password Cannot be Null", "Status":400, "Result":"Error"}
        return {"Message":"Password Suceffuly Changed", "Status":200, "Result":werkzeug.security.check_password_hash(self.password_hash, password_to_check)}
    
    def change_password(self, new_password:str):
        if(new_password != None):
            self.password_hash = werkzeug.security.generate_password_hash(new_password)
            return {"Message":"Password Suceffuly Changed", "Status":200, "Result":f"Password Changed to {new_password}"}
        else: return {"Message":"Password Cannot be Null", "Status":400, "Result":"Error"}