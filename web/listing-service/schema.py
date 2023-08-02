import re
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import Property as PropertyModel
from utils.googleMaps import geocodeBoundaries


class Property(SQLAlchemyObjectType):
    class Meta:
        model = PropertyModel
        interfaces = (graphene.relay.Node,)


class LatLngInput(graphene.InputObjectType):
    lat = graphene.Float()
    lng = graphene.Float()


class BoundaryInput(graphene.InputObjectType):
    southwest = graphene.InputField(LatLngInput)
    northeast = graphene.InputField(LatLngInput)


class FilterInput(graphene.InputObjectType):
    homeStatus = graphene.String()
    homeType = graphene.String()
    minPrice = graphene.Float()
    maxPrice = graphene.Float()
    noOfBedrooms = graphene.Int()
    noOfBathrooms = graphene.Float()
    minDaysOnZillow = graphene.Int()
    maxDaysOnZillow = graphene.Int()
    minLivingArea = graphene.Float()
    maxLivingArea = graphene.Float()


class PropertyQuery(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_properties = SQLAlchemyConnectionField(Property.connection)

    properties = graphene.List(Property)
    properties_by_terms = graphene.List(
        Property,
        address=graphene.String(description="input address"),
        boundary=graphene.Argument(BoundaryInput, description="input map boundary"),
        filters=graphene.Argument(FilterInput, description="property filters"),
    )

    def resolve_properties(self, info):
        query = Property.get_query(info)
        return query.all()

    def resolve_properties_by_terms(self, info, **args):
        query = Property.get_query(info)

        # search by address input (state, city, street address, zipcode)
        address = args.get("address")
        # exact match
        exact_property = query.filter(PropertyModel.street == address).first()
        if exact_property:
            return [exact_property]

        # fuzzy match
        fuzzy_properties = query.filter(PropertyModel.street.ilike(f"%{address}%"))

        # search by geocoding
        boundaries = geocodeBoundaries("San Francisco")  # default
        if address:
            boundaries = geocodeBoundaries(address)

        properties = query.filter(
            PropertyModel.latitude >= boundaries.southwest["lat"],
            PropertyModel.latitude <= boundaries.northeast["lat"],
            PropertyModel.longitude >= boundaries.southwest["lng"],
            PropertyModel.longitude <= boundaries.northeast["lng"],
        )

        properties = properties.union(fuzzy_properties)

        # search by map boundary
        boundary = args.get("boundary")
        if boundary:
            properties = properties.filter(
                PropertyModel.latitude >= boundary.southwest["lat"],
                PropertyModel.latitude <= boundary.northeast["lat"],
                PropertyModel.longitude >= boundary.southwest["lng"],
                PropertyModel.longitude <= boundary.northeast["lng"],
            )

        # search by filters
        filters = args.get("filters")
        if filters:
            if filters.get("homeStatus"):
                properties = properties.filter(
                    PropertyModel.homeStatus == filters.get("homeStatus")
                )
            if filters.get("homeType"):
                properties = properties.filter(
                    PropertyModel.homeType == filters.get("homeType")
                )
            if filters.get("minPrice"):
                properties = properties.filter(
                    PropertyModel.price >= filters.get("minPrice")
                )
            if filters.get("maxPrice"):
                properties = properties.filter(
                    PropertyModel.price <= filters.get("maxPrice")
                )
            if filters.get("noOfBedrooms"):
                properties = properties.filter(
                    PropertyModel.bed == filters.get("noOfBedrooms")
                )
            if filters.get("noOfBathrooms"):
                properties = properties.filter(
                    PropertyModel.bath == filters.get("noOfBathrooms")
                )
            if filters.get("minDaysOnZillow"):
                properties = properties.filter(
                    PropertyModel.daysOnZillow >= filters.get("minDaysOnZillow")
                )
            if filters.get("maxDaysOnZillow"):
                properties = properties.filter(
                    PropertyModel.daysOnZillow <= filters.get("maxDaysOnZillow")
                )
            if filters.get("minLivingArea"):
                properties = properties.filter(
                    PropertyModel.livingArea >= filters.get("minLivingArea")
                )
            if filters.get("maxLivingArea"):
                properties = properties.filter(
                    PropertyModel.livingArea <= filters.get("maxLivingArea")
                )

        return properties


schema = graphene.Schema(query=PropertyQuery)
