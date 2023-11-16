from operator import indexOf
import re
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Property as PropertyModel
from models import PropertyImage as PropertyImageModel
from models import Project as ProjectModel
from utils.googleMaps import geocodeBoundaries
import asyncio


class Property(SQLAlchemyObjectType):
    class Meta:
        model = PropertyModel
        interfaces = (graphene.relay.Node,)


class PropertyImage(SQLAlchemyObjectType):
    class Meta:
        model = PropertyImageModel
        interfaces = (graphene.relay.Node,)


class Project(SQLAlchemyObjectType):
    class Meta:
        model = ProjectModel
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


class ImgFilterInput(graphene.InputObjectType):
    zpid = graphene.Int()
    size = graphene.Int()
    format = graphene.String()


###################### Query ######################


class PropertyQuery(graphene.ObjectType):
    ######## Property Related Queries ########
    get_all_properties = graphene.List(Property)
    get_properties_by_terms = graphene.List(
        Property,
        address=graphene.String(description="input address"),
        boundary=graphene.Argument(
            BoundaryInput, description="input map boundary"),
        filters=graphene.Argument(FilterInput, description="property filters"),
    )
    get_property_images = graphene.List(
        PropertyImage, zpid=graphene.Int(description="zpid of the property")
    )
    get_property_images_by_size_format = graphene.List(
        PropertyImage,
        filters=graphene.Argument(
            ImgFilterInput, description="property image's zpid, size and format filters"),
    )
    get_property_by_zpid = graphene.List(
        Property,
        zpid=graphene.Int(description="zpid of the property")
    )

    ######## Resolovers for Property Related Queries ########
    def resolve_get_all_properties(self, info):
        query = Property.get_query(info)
        return query.all()

    def resolve_get_properties_by_terms(self, info, **args):
        query = Property.get_query(info)

        # search by address input (state, city, street address, zipcode)
        address = args.get("address")

        # Removed the below code, as it limits the number of resulting properties to 1.
        # # exact match
        # exact_property = query.filter(PropertyModel.street == address).first()
        # if exact_property:
        #     return [exact_property]

        # fuzzy match
        fuzzy_properties = query.filter(
            PropertyModel.street.ilike(f"%{address}%"))

        # search by geocoding
        # Async call to geocoding function
        boundaries = asyncio.run(geocodeBoundaries("San Francisco"))  # default
        if address:
            boundaries = asyncio.run(
                geocodeBoundaries(address))

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
                    PropertyModel.daysOnZillow >= filters.get(
                        "minDaysOnZillow")
                )
            if filters.get("maxDaysOnZillow"):
                properties = properties.filter(
                    PropertyModel.daysOnZillow <= filters.get(
                        "maxDaysOnZillow")
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

    def resolve_get_property_images(self, info, zpid):
        query = PropertyImage.get_query(info)
        image_urls = query.filter(PropertyImageModel.zpid == zpid).all()
        return image_urls

    def resolve_get_property_images_by_size_format(self, info, **args):
        query = PropertyImage.get_query(info)

    # TODO : NEED TO COMPLETE THE GRAPHQL QUERY TO GET THE IMAGEURLS BASED ON SIZE AND FORMAT FILTERS TO BE RENDERED ON THE CAROUSEL.
    # TODO : AND THEN A DIFFERENT SIZE/FORMAT WHEN A USER CLICKS ON THE PICTURE, TO GET A PROPER BIG VIEW
        filters = args.get("filters")
        zpid = filters.get("zpid")
        size = filters.get("size")  # Get size from filters argument
        format = filters.get("format")  # Get format from filters argument

        if zpid:
            query = query.filter(PropertyImageModel.zpid == zpid)

        if size and format:
            # Filter by size and format if both are provided
            query = query.filter(
                PropertyImageModel.imageURL.endswith(f'_{size}.{format}'))

        image_urls = query.all()
        return image_urls

    def resolve_get_property_by_zpid(self, info, zpid):
        query = Property.get_query(info)
        propertydetails = query.filter(PropertyModel.zpid == zpid).all()
        return propertydetails

    ######## Crowdfunding Project Related Queries ########
    get_all_projects = graphene.List(Project)

    # TODO: continue to add more terms for project selection
    get_projects_by_terms = graphene.List(
        Project,
        id=graphene.Int(description="id of the crowdfunding project"),
        propertyId=graphene.Int(
            description="property_id of the linked property"),
        isClose=graphene.Boolean(description="whether the project is closed"),
        maxTotalAmount=graphene.Float(
            description="max total amount of the project"),
        minTotalAmount=graphene.Float(
            description="min total amount of the project"),
        minDeposit=graphene.Float(
            description="minimum deposit of the project"),
        createdAfter=graphene.DateTime(description="created after this time"),
        closedBefore=graphene.DateTime(
            description="closed before of the project"),
        updatedAfter=graphene.DateTime(description="updated after this time"),
    )

    get_projects_by_investor = graphene.List(
        Project, investorEmail=graphene.String(
            description="auth_0 id of the investor")
    )

    ######## Resolovers for Project Related Queries ########
    def resolve_get_all_projects(self, info):
        query = Project.get_query(info)
        return query.all()

    def resolve_get_projects_by_terms(self, info, **args):
        query = Project.get_query(info)

        id = args.get("id")
        propertyId = args.get("propertyId")
        isClose = args.get("isClose")
        maxTotalAmount = args.get("maxTotalAmount")
        minTotalAmount = args.get("minTotalAmount")
        minDeposit = args.get("minDeposit")
        createdAfter = args.get("createdAfter")
        closedBefore = args.get("closedBefore")
        updatedAfter = args.get("updatedAfter")

        filters = {}
        if id:
            filters["id"] = id
        if propertyId:
            filters["property_id"] = propertyId
        if isClose:
            filters["isClose"] = isClose
        query = query.filter_by(**filters)

        if maxTotalAmount:
            query = query.filter(ProjectModel.totalAmount <= maxTotalAmount)
        if minTotalAmount:
            query = query.filter(ProjectModel.totalAmount >= minTotalAmount)
        if minDeposit:
            query = query.filter(ProjectModel.minDeposit >= minDeposit)
        if createdAfter:
            query = query.filter(ProjectModel.createdAt >= createdAfter)
        if closedBefore:
            query = query.filter(ProjectModel.closedAt <= closedBefore)
        if updatedAfter:
            query = query.filter(ProjectModel.updatedAt >= updatedAfter)

        results = query.all()
        return results

    def resolve_get_projects_by_investor(self, info, investorEmail):
        query = Project.get_query(info)
        projects = query.filter(
            ProjectModel.investors.contains([investorEmail])).all()
        return projects


schema = graphene.Schema(query=PropertyQuery)
