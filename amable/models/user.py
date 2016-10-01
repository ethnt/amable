# from amable import db
from amable.utils.password import hash_password
from datetime import datetime as dt
from sqlalchemy import event
from sqlalchemy.orm import relationship

# import amable.models

# from amable.models.post import Post
# from amable.models.report import Report
# from amable.models.postReport import PostReport
# from amable.models.postUpvote import PostUpvote

from amable.models import Base
from amable import db


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128))
    role = db.Column(db.String(10))
    bio = db.Column(db.Text)
    website = db.Column(db.String(128))
    location = db.Column(db.String(128))
    phone = db.Column(db.String(10))
    dob = db.Column(db.DateTime)
    profile_image = db.Column(db.String(128))
    date_created = db.Column(db.String(128), nullable=False)
    date_modified = db.Column(db.String(128), nullable=False)
    reports = relationship("Report", backref="user")
    posts = relationship("Post", backref="user")
    postReports = relationship("PostReport", backref="user")
    postUpvotes = relationship("PostUpvote", backref="user")


    def __init__(self,
                 username,
                 email,
                 password,
                 name,
                 bio,
                 website,
                 location,
                 phone,
                 dob,
                 profile_image=None,
                 role=None
                 ):

        self.username = username
        self.email = email

        # Hash the password. SHA256
        hashedPassword = hash_password(password)

        # Split the password and the salt
        splitPassword = hashedPassword.split(":")

        self.password = splitPassword[0]  # Password
        self.salt = splitPassword[1]     # Salt

        self.name = name

        if role is not None:
            self.role = role
        else:
            self.role = "user"

        self.bio = bio
        self.website = website
        self.location = location
        self.phone = phone
        self.dob = dob

        if profile_image is not None:
            self.profile_image = profile_image
        else:
            self.profile_image = ""

        now = dt.now()
        nowISO = now.isoformat()

        self.date_created = nowISO
        self.date_modified = nowISO

    def __repr__(self):
        return '<User %r>' % self.username


def after_insert_listener(mapper, connection, target):
        # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()


event.listen(User, 'after_update', after_insert_listener)