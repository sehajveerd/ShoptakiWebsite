from collections import OrderedDict
import unittest
from graphene.test import Client
from schema.user_schema import schema

from app import create_app, db


class TestUserSchema(unittest.TestCase):
    def setUp(self):
        self.app = create_app()  # Create the app instance
        self.client = Client(schema)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_create_user_mutation(self):
        print("Test create user mutation---------------")
        mutation = """
        mutation {
          createUser(auth0Id: "auth", emailId: "test@example.com", role: "default") {
            user {
              auth0Id
              emailId
              role
            }
          }
        }
        """
        executed = self.client.execute(mutation)
        expected = {
            "data": OrderedDict(
                [
                    (
                        "createUser",
                        {
                            "user": {
                                "auth0Id": "auth",
                                "emailId": "test@example.com",
                                "role": "default",
                            }
                        },
                    )
                ]
            )
        }
        print("Executed:", executed)
        print("Expected:", expected)
        self.assertDictEqual(executed, expected)

    def test_update_user_personal_details_mutation(self):
        print("Test update user personal details mutation---------------")
        mutation = """
        mutation {
          updatePersonalDetails(
            userId: "auth",
            firstName: "John",
            lastName: "Doe",
            address: "123 Main St",
            country: "USA",
            timezone: "UTC",
            phoneNumber: "1234567890",
            dateOfBirth: "1990-01-01"
          ) {
            user {
              auth0Id
              firstName
              lastName
              address
              country
              timezone
              phoneNumber
              dateOfBirth
            }
          }
        }
        """
        executed = self.client.execute(mutation)
        expected = {
            "data": OrderedDict(
                [
                    (
                        "updatePersonalDetails",
                        {
                            "user": {
                                "auth0Id": "auth",
                                "firstName": "John",
                                "lastName": "Doe",
                                "address": "123 Main St",
                                "country": "USA",
                                "timezone": "UTC",
                                "phoneNumber": "1234567890",
                                "dateOfBirth": "1990-01-01",
                            }
                        },
                    )
                ]
            )
        }
        print("Executed:", executed)
        print("Expected:", expected)
        self.assertEqual(executed, expected)

    # Add more test cases for other mutations and queries
    def test_user_detail_query(self):
        print("Test user detail query---------------")
        query = """
        query {
          userDetail(userId: "auth") {
            firstName
            lastName
            citizenshipStatus
            accountType
            hasInvestedBefore
            investmentReasons
          }
        }
        """
        executed = self.client.execute(query)
        # Define your expected result based on the query result structure
        expected = {
            "data": {
                "userDetail": {
                    "firstName": "John",
                    "lastName": "Doe",
                    "citizenshipStatus": None,  # Replace with expected value
                    "accountType": None,  # Replace with expected value
                    "hasInvestedBefore": None,  # Replace with expected value
                    "investmentReasons": None,  # Replace with expected value
                }
            }
        }
        print("Executed:", executed)
        print("Expected:", expected)
        self.assertDictEqual(executed, expected)

    def test_user_personal_details_query(self):
        print("Test user personal details query---------------")
        query = """
        query {
          userPersonalDetails(userId: "auth") {
            firstName
            lastName
            address
            country
            timezone
            phoneNumber
            dateOfBirth
          }
        }
        """
        executed = self.client.execute(query)
        # Define your expected result based on the query result structure
        expected = {
            "data": {
                "userPersonalDetails": {
                    "firstName": "John",
                    "lastName": "Doe",
                    "address": "123 Main St",
                    "country": "USA",
                    "timezone": "UTC",
                    "phoneNumber": "1234567890",
                    "dateOfBirth": "1990-01-01",
                }
            }
        }  # Define your expected result here
        print("Executed:", executed)
        print("Expected:", expected)
        self.assertDictEqual(executed, expected)


if __name__ == "__main__":
    unittest.main()
