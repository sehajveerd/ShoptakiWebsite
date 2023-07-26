import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import Property


class PropertyQuery(SQLAlchemyObjectType):
    class Meta:
        model = Property
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    '''
    sample query:
    query {
        properties {
            zpid
        }
    }
'''
    properties = graphene.List(PropertyQuery)

    def resolve_properties(self, info):
        print(info)
        query = PropertyQuery.get_query(info)
        return query.all()

schema = graphene.Schema(query=Query)

