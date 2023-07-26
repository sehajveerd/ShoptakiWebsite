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
            homeStatus=item["homeStatus"] if item["homeStatus"] != 'null' else None,
            homeType=item["homeType"] if item["homeType"] != 'null' else None,
            bed=int(float(item["bedrooms"])) if item["bedrooms"] != 'null' else None,
            bath=float(item["bathrooms"]) if item["bathrooms"] != 'null' else None,
            latitude=float(item["latitude"]) if item["latitude"] != 'null' else None,
            longitude=float(item["longitude"]) if item["longitude"] != 'null' else None,
            imageURI=item["imgSrc"] if item["imgSrc"] != 'null' else None,
            unit=item["unit"] if item["unit"] != 'null' else None,
            price=float(item["price"]) if item["price"] != 'null' else None,
            livingArea=float(item["livingArea"]) if item["livingArea"] != 'null' else None,
            lotAreaValue=float(item["lotAreaValue"]) if item["lotAreaValue"] != 'null' else None,
            lotAreaUnit=item["lotAreaUnit"] if item["lotAreaUnit"] != 'null' else None,
            zestimate=float(item["zestimate"]) if item["zestimate"] != 'null' else None,
            rentZestimate=float(item["rentZestimate"]) if item["rentZestimate"] != 'null' else None,
            zpid=int(float(item["zpid"])) if item["zpid"] != 'null' else None,
            daysOnZillow=int(float(item["daysOnZillow"])) if item["daysOnZillow"] != 'null' else None,
        )

        properties.append(property)
    return properties


def seed_properties():
    file = "../../datasets/Latest_maintable_output_4.csv"
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
