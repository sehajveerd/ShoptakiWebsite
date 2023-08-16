from googlemaps import Client
from config import Config


class Boundaries:
    def __init__(self):
        self.northeast = {"lat": None, "lng": None}
        self.southwest = {"lat": None, "lng": None}


# TODO: This api call should be coded in async way, but it seems to have a conflict with flask io.
def geocodeBoundaries(address):
    client = Client(key=Config.GOOGLE_MAPS_API_KEY)

    try:
        response = client.geocode(address, region="us")
        if response is not None:
            boundaries = Boundaries()
            boundaries.northeast["lat"] = float(
                response[0]["geometry"]["viewport"]["northeast"]["lat"]
            )
            boundaries.northeast["lng"] = float(
                response[0]["geometry"]["viewport"]["northeast"]["lng"]
            )
            boundaries.southwest["lat"] = float(
                response[0]["geometry"]["viewport"]["southwest"]["lat"]
            )
            boundaries.southwest["lng"] = float(
                response[0]["geometry"]["viewport"]["southwest"]["lng"]
            )
            return boundaries
        else:
            raise ValueError("Cannot find location from the input address")
    except Exception as e:
        raise ValueError("Error while retrieving address info")
