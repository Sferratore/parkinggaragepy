from datetime import datetime
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from xmlrpc.client import DateTime

from mock import GPIO
from mock.SDL_DS3231 import SDL_DS3231
from src.parking_garage import ParkingGarage
from src.parking_garage import ParkingGarageError

class TestParkingGarage(TestCase):

    @patch.object(GPIO, "input") # Stabilisco di voler fare mock della funzione "input" di GPIO
    def test_check_occupancy(self, mock_distance_sensor: Mock):
        mock_distance_sensor.return_value = True # Stabilisco che il valore di restituzione della funzione di "input" di GPIO sia true quando chiamata
        system = ParkingGarage() # Arrange
        occupied = system.check_occupancy(system.INFRARED_PIN1) # Act (dentro check_occupancy dovrà esserci la funzione input dic GPIO che verrà mock-ata a true)
        self.assertTrue(occupied) # Assert

    @patch.object(GPIO, "input")
    def test_check_number_occupied_spots(self, mock_distance_sensor: Mock):
        mock_distance_sensor.side_effect = [True, False, True] # Mock dell'uso di GPIO.input tre volte. Per dare un array di risultati diversi ogni chiamata va usato side_effect, return_value va bene solo per un valore costante.
        system = ParkingGarage()
        num = system.get_number_occupied_spots()
        self.assertEqual(num, 2)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_parking_fee_regular_days(self, mock_time_sensor: Mock):
        mock_time_sensor.return_value = datetime(2024, 11, 11, 15, 45)
        system = ParkingGarage()
        cost = system.calculate_parking_fee(datetime(2024, 11, 11, 12, 00))
        self.assertEqual(cost, 10)

