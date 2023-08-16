from .db import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)
    totalAmount = db.Column(db.Float, nullable=False, default=0)
    raisedAmount = db.Column(db.Float, nullable=False, default=0)
    riskRating = db.Column(db.Float, nullable=False, default=0)
    comments = db.Column(db.String)
    investors = db.Column(ARRAY(db.String(20)))
    numOfInvestors = db.Column(db.Integer, nullable=False, default=0)
    minDeposit = db.Column(db.Float, nullable=False, default=0)
    isClosed = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    closedAt = db.Column(db.DateTime)

    property = db.relationship(
        "Property", foreign_keys=[property_id], back_populates="project"
    )
