from models import db, Property, PropertyImage
import csv


def transform_dict_to_model(data_dict):
    images = []
    for property_zpid, image_list in data_dict.items():
        property = Property.query.filter_by(zpid=property_zpid).first()
        if property:
            for imageURL in image_list:
                images.append(
                    PropertyImage(zpid=int(float(property_zpid)), imageURL=imageURL)
                )
    return images


def seed_images():
    file = "../../datasets/property_image_urls.csv"
    images_dict = {}
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["zpid"]:
                zpid = int(row["zpid"])
                if zpid not in images_dict:
                    images_dict[zpid] = []

                images_dict[zpid].append(row["photo_urls"])

    images = transform_dict_to_model(images_dict)
    db.session.add_all(images)
    db.session.commit()


def delete_images():
    db.session.execute("TRUNCATE property_images RESTART IDENTITY CASCADE;")
    db.session.commit()
