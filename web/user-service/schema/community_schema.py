import graphene
from datetime import datetime
from models.community import Channel, Message
from models import db


class ChannelType(graphene.ObjectType):
    class Meta:
        model = Channel
        interfaces = (graphene.relay.Node,)


class MessageType(graphene.ObjectType):
    class Meta:
        model = Message
        interfaces = (graphene.relay.Node,)


###################### mutations ######################
class CreateChannel(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        creator_id = graphene.String(required=True)
        property_id = graphene.Int(required=True)

    channel = graphene.Field(ChannelType)

    def mutate(self, info, id, name, creator_id, property_id):
        new_channel = Channel(
            id=id, name=name, creator_id=creator_id, property_id=property_id
        )
        db.session.add(new_channel)
        db.session.commit()

        return CreateChannel(channel=new_channel)


class CreateMessage(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        text = graphene.String(required=True)
        sender_id = graphene.String(required=True)
        channel_id = graphene.Int(required=True)

    message = graphene.Field(MessageType)

    def mutate(self, info, id, text, sender_id, channel_id):
        new_message = Message(
            id=id, text=text, sender_id=sender_id, channel_id=channel_id
        )
        db.session.add(new_message)
        db.session.commit()

        return CreateMessage(message=new_message)


class UpdateChannel(graphene.Mutation):
    class Arguments:
        channelId = graphene.String(required=True)

    channel = graphene.Field(ChannelType)

    def mutate(self, info, channelId):
        # Implement the logic to update a user's personal details in the database
        channel = Channel.query.filter_by(id=channelId).first()
        channel.updated_at = datetime.utcnow()
        db.session.commit()

        return UpdateChannel(channel=channel)


###################### queries ######################
class Query(graphene.ObjectType):
    channel = graphene.Field(ChannelType, channelId=graphene.Int(required=True))

    def resolve_channel(self, info, channelId):
        channel = Channel.query.filter_by(id=channelId).first()
        if channel:
            (
                id,
                name,
                description,
                created_at,
                updated_at,
                creator_id,
                property_id,
            ) = channel

            # Get the associated property name
            property = Property.query.filter_by(id=property_id).first()
            if property:
                property_name = property.street
            else:
                property_name = None

            channel_info = ChannelType(
                name=name,
                description=description,
                created_at=created_at,
                updated_at=updated_at,
                creator_id=creator_id,
                property_name=property_name,
            )

            return channel_info
        else:
            return None

    messages = graphene.List(MessageType, messageId=graphene.Int(required=True))

    def resolve_messages(self, info, messageId):
        messages = Message.query.filter_by(
            id=messageId
        ).all()  # Retrieve all messages with the given ID
        if messages:
            message_list = []
            for message in messages:
                id, text, created_at, channel_id, sender_id = message

                # Get the associated channel name
                channel = Channel.query.filter_by(id=channel_id).first()
                if channel:
                    channel_name = channel.name
                else:
                    channel_name = None

                message_info = MessageType(
                    text=text,
                    created_at=created_at,
                    channel_name=channel_name,  # Include the channel name instead of channel_id
                    sender_id=sender_id,
                )
                message_list.append(message_info)

            return message_list
        else:
            return None


###################### schema ######################
class Mutation(graphene.ObjectType):
    createUser = CreateChannel.Field()
    CreateMessage = CreateMessage.Field()
    UpdateChannel = UpdateChannel.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
