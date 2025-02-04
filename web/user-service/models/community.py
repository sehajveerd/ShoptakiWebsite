import datetime
from .db import db


class Channel(db.Model):
    __tablename__ = "channels"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    creator_id = db.Column(db.String, db.ForeignKey("users.id"))
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"))


class Message:
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"))
    sender_id = db.Column(db.String, db.ForeignKey("users.id"))
