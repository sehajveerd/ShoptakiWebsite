import csv
from models import db, Property, State
from sqlalchemy.sql import text


def get_state_id(state_name):
    state = State.query.filter_by(state=state_name).first()
    if state:
        return state.id
    else:
        return None


def transform_dict_to_model(data_dict):
    properties = []
    for item in data_dict:
        property = Property(
            street=item["streetAddress"],
            city=item["city"],
            zipcode=item["zipcode"],
            state_id=get_state_id(item["state"]),
            homeStatus=item["homeStatus"] if item["homeStatus"] != "" else None,
            homeType=item["homeType"] if item["homeType"] != "" else None,
            bed=int(float(item["bedrooms"])
                    ) if item["bedrooms"] != "" else None,
            bath=float(item["bathrooms"]) if item["bathrooms"] != "" else None,
            latitude=float(item["latitude"]
                           ) if item["latitude"] != "" else None,
            longitude=float(item["longitude"]
                            ) if item["longitude"] != "" else None,
            imageURI=item["imgSrc"] if item["imgSrc"] != "" else None,
            unit=item["unit"] if item["unit"] != "" else None,
            price=float(item["price"]) if item["price"] != "" else None,
            livingArea=float(item["livingArea"]
                             ) if item["livingArea"] != "" else None,
            zestimate=float(item["zestimate"]
                            ) if item["zestimate"] != "" else None,
            rentZestimate=float(item["rentZestimate"])
            if item["rentZestimate"] != ""
            else None,
            zpid=int(float(item["zpid"])) if item["zpid"] != "" else None,
            daysOnZillow=int(float(item["daysOnZillow"]))
            if item["daysOnZillow"] != ""
            else None,
            description=item["description"] if item["description"] != "" else None,
        )

        properties.append(property)
    return properties


def seed_properties():
    file = "../../datasets/properties_cleaned.csv"
    properties_dict = []
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            properties_dict.append(row)

    properties = transform_dict_to_model(properties_dict)
    db.session.add_all(properties)
    db.session.commit()


def delete_properties():
    db.session.execute(text("TRUNCATE properties RESTART IDENTITY CASCADE;"))
    db.session.commit()
