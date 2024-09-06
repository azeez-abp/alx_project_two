import unittest
import uuid
from unittest.mock import patch

import flask
from sqlalchemy import select

from app.app import app
from app.libs.password import hash_password
from app.models.schemas.general.address import Addresses
from app.models.schemas.users.user import Users
from app.models.storage_engine import storage


class UserLoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        user_id = uuid.uuid4()
        self.user_addr = {
            "user_id": user_id,
            "street": "yejide",
            "city": "Ibadan",
            "state": "Oyo",
            "zip_code": "2000525",
        }

        new_address = Addresses(
            user_id=self.user_addr["user_id"],
            street=self.user_addr["street"],
            city=self.user_addr["city"],
            state=self.user_addr["state"],
            zip_code=self.user_addr["zip_code"],
        )

        data_all = {
            "user_id": user_id,
            "first_name": "Azeez",
            "profile_image": "uploads/4750c7bf-50a1-4148-93ad-cad1ea7f\
                6218.jpg",
            "middle_name": "Adio",
            "last_name": "Ade",
            "email": str(user_id) + "@gmail.com",
            "password": "uYmFDUVBwVm9Zb",
            "gender": "Male",
            "date_of_birth": "1998-06-07",
        }

        new_user = Users(
            user_id=data_all["user_id"],
            first_name=data_all["first_name"],
            profile_pix=data_all["profile_image"],  # Corrected attribute name
            middle_name=data_all["middle_name"],
            last_name=data_all["last_name"],
            email=data_all["email"],
            password=hash_password(data_all["password"]),
            gender=data_all["gender"],
            date_of_birth=data_all["date_of_birth"],
            addresses=[new_address],
        )

        # Setup a user in the mock database
        with self.app.app_context():
            storage.get_instance().add(new_user)  # Corrected method call
            storage.get_instance().commit()
            self.user = storage.get_instance().scalar(
                select(Users).where(Users.email == data_all["email"])
            )

            self.user_data = {
                "email": data_all["email"],  # Corrected key name
                "password": data_all["password"],  # Corrected key name
                "user_id": self.user.user_id,
            }

    def test_user_added(self):
        self.assertIsNotNone(self.user)

    def tearDown(self):
        # Clear the mock database
        with self.app.app_context():
            storage.get_instance().query(Users).filter(
                Users.user_id == self.user_data.get("user_id")
            ).delete()
            storage.get_instance().commit()

    def test_login_success(self):
        response = self.client.post("/api/v1/users/login", json=self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("User login successful", response.json["success"])

    def test_login_failure(self):
        wrong_data = {"email": "wrong@example.com", "password": "wrong_password"}
        response = self.client.post(
            "api/v1/users/login", json=wrong_data
        )  # Corrected route
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "User with email wrong@example.com not found", response.json["error"]
        )


class TestLogin(unittest.TestCase):
    @patch("app.models.storage_engine.storage.get_instance")
    def setUp(self, mock_storage):
        self.app = app
        self.client = self.app.test_client()

        # Mock data for user
        self.user_data = {
            "user_id": "8daec549-8c0d-42dd-9352-22b4ca900a97",
            "email": "test@example.com",
            "password": "test_password",
        }

        # Create a mock user object
        self.mock_user = Users(
            user_id=self.user_data["user_id"],
            email=self.user_data["email"],
            password=hash_password(self.user_data["password"]),
        )

        # Mock the storage engine's add and commit methods
        mock_storage.return_value.add.return_value = None
        mock_storage.return_value.commit.return_value = None

        # Mock the storage engine's scalar method to return the mock user
        mock_storage.return_value.scalar.return_value = self.mock_user

    def test_create_app(self):
        """check app instance with blueprint is created"""
        with app.test_client() as c:
            self.assertIsInstance(c, flask.testing.FlaskClient)


if __name__ == "__main__":
    unittest.main()
