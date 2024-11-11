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

    @patch.object(SDL_DS3231, "read_datetime")
    def test_parking_fee_weekend_days(self, mock_time_sensor: Mock):
        mock_time_sensor.return_value = datetime(2024, 11, 10, 15, 45)
        system = ParkingGarage()
        cost = system.calculate_parking_fee(datetime(2024, 11, 10, 12, 00))
        self.assertEqual(cost, 12.5)

    @patch.object(ParkingGarage, "change_servo_angle")
    def test_open_garage_door(self, mock_servo: Mock):
        system = ParkingGarage()
        system.open_garage_door()
        mock_servo.assert_called_with(12) # Controlla che il metodo change_servo_angle venga usato con argomento "12". Genera assertionerror se non succede!
        self.assertTrue(system.open_garage_door) # Questo qui da sempre true se il metodo esiste

    @patch.object(ParkingGarage, "change_servo_angle")
    def test_closed_garage_door(self, mock_servo: Mock):
        system = ParkingGarage()
        system.close_garage_door()
        mock_servo.assert_called_with(0)  # Controlla che il metodo change_servo_angle venga usato con argomento "12". Genera assertionerror se non succede!
        self.assertTrue(system.close_garage_door)  # Questo qui da sempre true se il metodo esiste

    def test_red_light_on(self):
        system = ParkingGarage()
        system.turn_on_red_light()
        self.assertTrue(system.red_light_on)

    def test_red_light_off(self):
        system = ParkingGarage()
        system.red_light_on = True
        system.turn_off_red_light()
        self.assertTrue(not system.red_light_on)