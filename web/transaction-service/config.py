import os


class Config:
    STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY")
    CLOUDAMQP_URL = os.environ.get("CLOUDAMQP_URL")
