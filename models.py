"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)



class USER(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.Text,
                           nullable=False)

    last_name = db.Column(db.Text,
                           nullable=False)
    
    img_url = db.Column(
                        db.Text,
                        nullable=False,
                        default='https://pbs.twimg.com/media/E-wB_MRXMAczerU.jpg'
                        )
    
    @property
    def full_name(self):
        return f'{self.first_name}  {self.last_name}'