from .db import db


class UserDetail(db.Model):
    __tablename__ = "user_details"

    auth0_id = db.Column(db.String(20), primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    email_id = db.Column(db.String(50), nullable=False)
    firstName = db.Column(db.String(30))
    lastName = db.Column(db.String(30))
    address = db.Column(db.String(100))
    city = db.Column(db.String(30))
    country = db.Column(db.String(20))
    zipcode = db.Column(db.String(5))
    timezone = db.Column(db.String(30))
    phoneNumber = db.Column(db.String(20))
    dateOfBirth = db.Column(db.String(10))
    citizenshipStatus = db.Column(db.String(20))  # to be mapped to enum
    ssnNumber = db.Column(db.String(20))
    accountType = db.Column(db.Integer)  # to be mapped to enum
    estimatedNetWorth = db.Column(db.Integer)
    investmentExperience = db.Column(db.String)
    hasInvestedBefore = db.Column(db.String)
    investmentReasons = db.Column(db.String(20))
    investedProjects = db.Column(db.String)

    channels = db.relationship("Channel", back_populates="user")
