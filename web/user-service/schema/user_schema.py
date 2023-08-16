import graphene
from models.userDetail import UserDetail
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import db

class UserDetailType(SQLAlchemyObjectType):
    class Meta:
        model = UserDetail
        interfaces = (graphene.relay.Node, )

###################### mutations ######################
class CreateUser(graphene.Mutation):
    class Arguments:
        auth0Id = graphene.String(required = True)
        emailId = graphene.String(required = True)
        role = graphene.String(required = True)

    user = graphene.Field(UserDetailType)

    def mutate(self, info, auth0Id, emailId, role):
        # Implement the logic to create a new user in the database
        new_user = UserDetail(auth0_id = auth0Id, email_id = emailId, role = role)
        db.session.add(new_user)
        db.session.commit()

        return CreateUser(user = new_user)


class UpdateUserPersonalDetails(graphene.Mutation):
    class Arguments:
        userId = graphene.String(required = True)
        firstName = graphene.String()
        lastName = graphene.String()
        address = graphene.String()
        country = graphene.String()
        timezone = graphene.String()
        phoneNumber = graphene.String()
        dateOfBirth = graphene.String()

    user = graphene.Field(UserDetailType)

    def mutate(self, info, userId, firstName, lastName, address, country, timezone, phoneNumber, dateOfBirth):
        # Implement the logic to update a user's personal details in the database
        user = UserDetail.query.filter_by(auth0_id = userId).first()
        user.firstName = firstName
        user.lastName = lastName
        user.address = address
        user.country = country
        user.timezone = timezone
        user.phoneNumber = phoneNumber
        user.dateOfBirth = dateOfBirth
        db.session.commit()

        return UpdateUserPersonalDetails(user = user)


class UpdateUserFinanceDetails(graphene.Mutation):
    class Arguments:
        userId = graphene.String(required = True)
        citizenshipStatus = graphene.String()
        ssnNumber = graphene.String()
        accountType = graphene.String()
        estimatedNetWorth = graphene.Int()

    user = graphene.Field(UserDetailType)

    def mutate(self, info, userId, citizenshipStatus, ssnNumber, accountType, estimatedNetWorth):
        # Implement the logic to update a user's finance details in the database
        user = UserDetail.query.filter_by(auth0_id = userId).first()
        user.citizenshipStatus = citizenshipStatus
        user.ssnNumber = ssnNumber
        user.accountType = accountType
        user.estimatedNetWorth = estimatedNetWorth
        db.session.commit()

        return UpdateUserFinanceDetails(user = user)
    
class UpdateUserInvestmentExperience(graphene.Mutation):
    class Arguments:
        userId = graphene.String(required = True)
        investmentExperience = graphene.String()
        hasInvestedBefore = graphene.String()
        investmentReasons = graphene.String()

    user = graphene.Field(UserDetailType)

    def mutate(self, info, userId, investmentExperience, hasInvestedBefore):
        # Implement the logic to update a user's investment experience in the database
        user = UserDetail.query.filter_by(auth0_id = userId).first()
        user.investmentExperience = investmentExperience
        user.hasInvestedBefore = hasInvestedBefore
        db.session.commit()

        return UpdateUserInvestmentExperience(user = user)
    
class UpdateUserInvestmentReasons(graphene.Mutation):
    class Arguments:
        userId = graphene.String(required = True)
        investmentReasons = graphene.String()

    user = graphene.Field(UserDetailType)

    def mutate(self, info, userId, investmentReasons):
        # Implement the logic to update a user's investment reasons in the database
        user = UserDetail.query.filter_by(auth0_id = userId).first()
        user.investmentReasons = investmentReasons
        db.session.commit()

        return UpdateUserInvestmentReasons(user = user)

###################### queries ######################
class Query(graphene.ObjectType):
    user_detail = graphene.Field(UserDetailType, userId = graphene.String(required = True))

    def resolve_user_detail(self, info, userId):
        # Implement the logic to fetch a user detail by auth0_id from the database
        user_detail = UserDetail.query.filter_by(auth0_id = userId).with_entities(
        UserDetail.firstName,
        UserDetail.lastName,
        UserDetail.citizenshipStatus,
        UserDetail.accountType,
        UserDetail.hasInvestedBefore,
        UserDetail.investmentReasons
        ).first()
        if user_detail:
            first_name, last_name, citizenship_status, account_type, has_invested_before, investment_reasons = user_detail

            user_detail = UserDetailType(
                firstName=first_name,
                lastName=last_name,
                citizenshipStatus=citizenship_status,
                accountType=account_type,
                hasInvestedBefore=has_invested_before,
                investmentReasons=investment_reasons
            )

            return user_detail
        else:
            return None

    # Add the getUserPersonalDetails query
    user_personal_details = graphene.Field(UserDetailType, userId=graphene.String(required = True))

    def resolve_user_personal_details(self, info, userId):
        # Implement the logic to fetch user's personal details by userId from the database
        user_personal_details = UserDetail.query.filter_by(auth0_id = userId).with_entities(
        UserDetail.firstName,
        UserDetail.lastName,
        UserDetail.address,
        UserDetail.country,
        UserDetail.timezone,
        UserDetail.phoneNumber,
        UserDetail.dateOfBirth
        ).first()
        if user_personal_details:
            first_name, last_name, address, country, timezone, phoneNumber, dateOfBirth = user_personal_details

            user_personal_details = UserDetailType(
                firstName=first_name,
                lastName=last_name,
                address=address,
                country=country,
                timezone=timezone,
                phoneNumber=phoneNumber,
                dateOfBirth=dateOfBirth
            )

            return user_personal_details
        else:
            return None

    # Add the getUserFinanceDetails query
    user_finance_details = graphene.Field(UserDetailType, auth0_id=graphene.String(required = True))

    def resolve_user_finance_details(self, info, auth0Id):
        # Implement the logic to fetch user's finance details by userId from the database
        user_finance_details = UserDetail.query.filter_by(auth0_id = auth0Id).with_entities(
        UserDetail.citizenshipStatus,
        UserDetail.ssnNumber,
        UserDetail.accountType,
        UserDetail.estimatedNetWorth
        ).first()

        if user_finance_details:
            citizenship_status, ssn_number, account_type, estimated_net_worth = user_finance_details

            user_finance_details = UserDetailType(
                citizenshipStatus=citizenship_status,
                ssnNumber=ssn_number,
                accountType=account_type,
                estimatedNetWorth=estimated_net_worth
            )

            return user_finance_details
        else:
            return None

    # Add the getUserInvestmentExperience query
    user_investment_experience = graphene.Field(UserDetailType, auth0_id=graphene.String(required = True))

    def resolve_user_investment_experience(self, info, auth0Id):
        # Implement the logic to fetch user's investment experience details by userId from the database
        user_investment_experience = UserDetail.query.filter_by(auth0_id = auth0Id).with_entities(
        UserDetail.hasInvestedBefore,
        UserDetail.investmentExperienceLevel
        ).first()
        
        if user_investment_experience:
            has_invested_before, investment_experience_level = user_investment_experience

            user_investment_experience = UserDetailType(
                hasInvestedBefore=has_invested_before,
                investmentExperienceLevel=investment_experience_level
            )

            return user_investment_experience
        else:
            return None
    
    # Add the getUserInvestmentReason query
    user_investment_reason = graphene.Field(UserDetailType, auth0_id=graphene.String(required = True))

    def resolve_user_investment_reason(self, info, auth0Id):
        # Implement the logic to fetch user's investment reason details by userId from the database
        user_investment_reason = UserDetail.query.filter_by(auth0_id = auth0Id).with_entities(
        UserDetail.investmentReasons
        ).first()
        
        if user_investment_reason:
            investment_reasons = user_investment_reason

            user_investment_reason = UserDetailType(
                investmentReasons=investment_reasons
            )

            return user_investment_reason
        else:
            return None


###################### schema ######################
class Mutation(graphene.ObjectType):
    createUser = CreateUser.Field()
    updatePersonalDetails = UpdateUserPersonalDetails.Field()
    updateFinanceDetails = UpdateUserFinanceDetails.Field()
    updateInvestmentExperience = UpdateUserInvestmentExperience.Field()
    updateInvestmentReasons = UpdateUserInvestmentReasons.Field()


schema = graphene.Schema(query = Query, mutation = Mutation)