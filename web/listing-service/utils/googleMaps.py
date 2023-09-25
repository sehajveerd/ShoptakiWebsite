from googlemaps import Client
from config import Config
# Added by VSW - Start
from aiohttp import ClientSession
# Added by VSW - End


class Boundaries:
    def __init__(self):
        self.northeast = {"lat": None, "lng": None}
        self.southwest = {"lat": None, "lng": None}


# TODO: This api call should be coded in async way, but it seems to have a conflict with flask io.
###############          DONE         #################

# Code for Asynchronous API Call to Geocoding API
async def geocodeBoundaries(address):
    async with ClientSession() as session:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={Config.GOOGLE_MAPS_API_KEY}"

        async with session.get(url) as response:
            data = await response.json()
            print(data)

            if data.get("status") == "OK":
                results = data.get("results")
                if results:
                    location = results[0]["geometry"]["viewport"]
                    boundaries = Boundaries()
                    boundaries.northeast["lat"] = location["northeast"]["lat"]
                    boundaries.northeast["lng"] = location["northeast"]["lng"]
                    boundaries.southwest["lat"] = location["southwest"]["lat"]
                    boundaries.southwest["lng"] = location["southwest"]["lng"]
                    return boundaries
                else:
                    raise ValueError(
                        "Cannot find location from the input address")
            else:
                raise ValueError("Error while retrieving address info")
