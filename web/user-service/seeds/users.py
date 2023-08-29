from models import db, UserDetail
import csv


def seed_users():
    file = "../../datasets/users_sample.csv"
    users = []
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user = UserDetail(
                auth0_id=row["auth0_id"],
                role=row["role"],
                email_id=row["email_id"],
                firstName=row["firstName"],
                lastName=row["lastName"],
                address=row["address"],
                city=row["city"],
                country=row["country"],
                zipcode=row["zipcode"],
                timezone=row["timezone"],
                phoneNumber=row["phoneNumber"],
                dateOfBirth=row["dateOfBirth"],
                citizenshipStatus=row["citizenshipStatus"],
                ssnNumber=row["ssnNumber"],
                accountType=int(row["accountType"]),  # Convert to integer
                estimatedNetWorth=int(row["estimatedNetWorth"]),  # Convert to integer
                investmentExperience=row["investmentExperience"],
                hasInvestedBefore=row["hasInvestedBefore"],
                investmentReasons=row["investmentReasons"],
            )
            users.append(user)

    db.session.add_all(users)
    db.session.commit()


def delete_users():
    db.session.execute("TRUNCATE user_details RESTART IDENTITY CASCADE;")
    db.session.commit()
