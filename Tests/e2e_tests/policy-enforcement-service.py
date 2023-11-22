import unittest
import requests
import logging
import pydantic
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from dotenv import load_dotenv
from os import environ
from typing import Any
import config


cfg: config.Config = config.load_config()

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-9s | %(message)s"
)

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json()}'
)

#policy-enforcement-service
ENTRYPOINT = cfg.POLICY_SERVICE_ENTRYPOINT
DATABASE_DSN = str(cfg.POSTGRES_DSN)
DATABASE_SCHEMA = "users"

ACCESS_DENIED_MESSAGE = {'message': 'Content not found'}
ADMIN_GROUP_ID = 3
SELLER_GROUP_ID = 2
CUSTOMER_GROUP_ID = 1


class User(pydantic.BaseModel):
    id: str
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    username: str
    group_id: int


class TestCommonFunctionality(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_service_availability(self):
        response = requests.get(ENTRYPOINT + "145gkajgsajgjg")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)


class BaseUserTestCase(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.test_user: User = None
        self.access_token: str = None

    def setUp(self, group_id: int) -> None:
        self._register_test_user(group_id)
        self._login()

    def tearDown(self) -> None:
        self._delete_test_user()

    def _register_test_user(self, group_id: int) -> User:
        payload = {
            "email": "test_user_example@example.com",
            "password": "password",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "username",
            "group_id": group_id
        }
        try:
            logger.info("Running request")
            response = requests.post(f'{ENTRYPOINT}auth/register', json=payload)
            response.raise_for_status()
            self.test_user = User(**response.json())
        except requests.exceptions.HTTPError as exc:
            logger.error(exc.response.text)
            logger.error(exc)

    def _raise_if_invalid_user(self):
        if self.test_user is None:
            raise Exception('Cannot continue test without valid user!')

    def _delete_test_user(self):
        if self.test_user is None:
            return
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            connection.execute(text(f"""DELETE FROM "{DATABASE_SCHEMA}"."user" WHERE id = '{self.test_user.id}';"""))
            connection.commit()

    def _set_superuser(self, is_superuser: bool):
        if self.test_user is None:
            return
        self.test_user.is_superuser = is_superuser
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            connection.execute(text(
                f"""UPDATE "{DATABASE_SCHEMA}"."user" SET is_superuser = {self.test_user.is_superuser} WHERE id = '{self.test_user.id}';"""))
            connection.commit()

    def _login(self):
        self._raise_if_invalid_user()
        try:
            data = {
                'username': 'test_user_example@example.com',
                'password': 'password',
            }
            response = requests.post(
                f'{ENTRYPOINT}auth/jwt/login', data=data
            )
            response.raise_for_status()
            self.access_token = response.json()['access_token']
        except requests.exceptions.HTTPError as exc:
            logger.error(exc)

    @property
    def auth_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}'
        }


class TestAdminPolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp(ADMIN_GROUP_ID)
        self._set_superuser(True)
        self._login()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_groups_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}groups', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)


class TestSellerPolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp(SELLER_GROUP_ID)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_groups_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}groups', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)

    def test_get_favorites_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}favorites', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)

    def test_get_apartments_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}apartments', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_reviews_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}reviews?apartment_id=5&skip=0&limit=10', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_reservations_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}reservations', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)



class TestCustomerPolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp(CUSTOMER_GROUP_ID)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_groups_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}groups', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)

    def test_get_favorites_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}favorites?user_email=user%40mail.ru&limit=1&offset=0', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_apartments_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}apartments', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_reviews_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}reviews?apartment_id=5&skip=0&limit=10', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_reservations_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}reservations', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()