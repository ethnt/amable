from amable import db
from datetime import datetime as dt
from sqlalchemy import event
from sqlalchemy.orm import relationship

# import models

# from models.postReport import PostReport
# from models.postUpvote import PostUpvote

from models.base import Base

class Post(Base):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    text_brief = db.Column(db.String(142))
    text_long = db.Column(db.Text)
    answered = db.Column(db.Boolean)
    hashtags = db.Column(db.Text)
    image_url = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    reports = relationship("PostReport", backref="post")
    postUpvotes = relationship("PostUpvote", backref="post")

    def __init__(
            self,
            text_brief,
            text_long,
            hashtags,
            image_url,
            user_id,
            community_id,
            answered = 0
    ):
        self.text_brief = text_brief
        self.text_long = text_long
        self.answered = answered
        self.hashtags = hashtags
        self.image_url = image_url
        self.user_id = user_id
        self.community_id = community_id

        # Default Values
        now = dt.now().isoformat  # Current Time to Insert into Datamodels.base
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Post %r>' % self.id


def after_insert_listener(mapper, connection, target):
        # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Post, 'after_update', after_insert_listener)