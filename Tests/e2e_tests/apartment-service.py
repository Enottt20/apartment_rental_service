import unittest
import logging

import requests
from pydantic import BaseModel
from typing import Optional
import config

APARTMENT_DELETED_MESSAGE = {"message": "Item successfully deleted"}
APARTMENT_NOT_FOUND_MESSAGE = {"detail": "Not Found"}


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-9s | %(message)s"
)


cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json()}'
)

ENTRYPOINT = cfg.APARTMENT_SERVICE_ENTRYPOINT



class Apartment(BaseModel):
    id: int
    title: str
    address: str
    rooms: int
    area: int
    latitude: float
    longitude: float


class ApartmentsQuery(BaseModel):
    city_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    radius: Optional[float]
    limit: int = 1
    offset: int = 0


apartments = [
    {
        "id": "1",
        "title": "title1",
        "address": "address1",
        "rooms": "1",
        "area": "1",
        "latitude": "1",
        "longitude": "1",
    },
    {
        "id": "2",
        "title": "title2",
        "address": "address2",
        "rooms": "2",
        "area": "2",
        "latitude": "2",
        "longitude": "2",
    },
]


class TestCase(unittest.TestCase):
    def _create_apartment(self, payload: Apartment = apartments[0]) -> Apartment:

        response = requests.post(f"{ENTRYPOINT}apartments", json=payload)
        self.assertEqual(response.status_code, 201)
        return Apartment(**response.json())

    def _update_apartment(self, apartment_id, payload: Apartment = apartments[1]) -> Apartment:

        response = requests.put(f"{ENTRYPOINT}apartments/{apartment_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        return Apartment(**response.json())

    def _del_apartment(self, apartment_id) -> requests.Response:
        response = requests.delete(f"{ENTRYPOINT}apartments/{apartment_id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), APARTMENT_DELETED_MESSAGE)
        return response

    def test_service_availability(self):
        response = requests.get(ENTRYPOINT + "145gkajgsajgjg")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, APARTMENT_NOT_FOUND_MESSAGE)

    def test_get_apartments(self, limit=10, offset=0):
        payload = {
            "limit": limit,
            "offset": offset
        }
        response = requests.get(f"{ENTRYPOINT}apartments", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_add_apartment(self):
        data = self._create_apartment()
        try:
            self.assertIsInstance(data, Apartment)
            self.assertEqual(data, Apartment(**apartments[0]))
        except requests.exceptions.HTTPError as exc:
            logger.error(exc.response.text)
            logger.error(exc)
        finally:
            self._del_apartment(data.id)

    def test_update_apartment(self):
        data = self._create_apartment()
        try:
            data = self._update_apartment(1)
            self.assertIsInstance(data, Apartment)
            self.assertEqual(data, Apartment(**apartments[1]))

        finally:
            self._del_apartment(data.id)
