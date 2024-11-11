from datetime import datetime
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
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
        mock_distance_sensor.return_value = [True, False, True] # Mock dell'uso di GPIO.input tre volte
        system = ParkingGarage()
        num = system.get_number_occupied_spots()
        self.assertEqual(num, 2)



