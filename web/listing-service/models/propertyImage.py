from .db import db


class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id = db.Column(db.Integer, primary_key=True)
    zpid = db.Column(db.Integer, db.ForeignKey("properties.zpid"), nullable=False)
    imageURL = db.Column(db.String, nullable=False)

    property = db.relationship("Property", back_populates="images")
