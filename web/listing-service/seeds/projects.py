from models import db, Project
import csv
from datetime import datetime


def seed_projects():
    file = "../../datasets/projects_sample.csv"
    projects = []
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            project = Project(
                property_id=int(row["property_id"]),
                totalAmount=float(row["totalAmount"]),
                raisedAmount=float(row["raisedAmount"])
                if row["raisedAmount"]
                else None,
                riskRating=float(row["riskRating"]),
                comments=row["comments"],
                minDeposit=float(row["minDeposit"]),
                isClosed=bool(row["isClosed"]),
                createdAt=datetime.strptime(row["createdAt"], "%Y-%m-%d %H:%M:%S"),
                updatedAt=datetime.strptime(
                    row["updatedAt"], "%Y-%m-%d %H:%M:%S"
                ),  # timestamp of the most recent transaction
                closedAt=datetime.strptime(row["closedAt"], "%Y-%m-%d %H:%M:%S")
                if row["closedAt"]
                else None,
            )
            projects.append(project)

    db.session.add_all(projects)
    db.session.commit()


def delete_projects():
    db.session.execute("TRUNCATE projects RESTART IDENTITY CASCADE;")
    db.session.commit()
