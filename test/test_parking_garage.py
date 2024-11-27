from datetime import datetime
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from xmlrpc.client import DateTime

from mock import GPIO
from mock.SDL_DS3231 import SDL_DS3231
from src.parking_garage import ParkingGarage
from src.parking_garage import ParkingGarageError


# NOTA: In questa classe di test non è presente un DUMMY OBJECT.
# Ipotesi: un dummy object potrebbe essere utilizzato se ParkingGarage accettasse, ad esempio,
# un logger come dipendenza, e quel logger non fosse rilevante per il test.
# Ad esempio:
#
# class DummyLogger:
#     def info(self, message):
#         pass
#     def error(self, message):
#         pass
#
# E il ParkingGarage potrebbe essere inizializzato con:
# dummy_logger = DummyLogger()
# system = ParkingGarage(logger=dummy_logger)
class TestParkingGarage(TestCase):

    # ESEMPIO DI TEST STUB (Replacement di INPUT INDIRETTO)
    @patch.object(GPIO, "input") # Stabilisco di voler fare mock della funzione "input" di GPIO. Questo è un test stub (responder).
    def test_check_occupancy(self, mock_distance_sensor: Mock):
        mock_distance_sensor.return_value = True # Stabilisco che il valore di restituzione della funzione di "input" di GPIO sia true quando chiamata
        system = ParkingGarage() # Arrange
        occupied = system.check_occupancy(system.INFRARED_PIN1) # Act (dentro check_occupancy dovrà esserci la funzione input dic GPIO che verrà mock-ata a true)
        self.assertTrue(occupied) # Assert

    # ESEMPIO DI TEST STUB (Replacement di INPUT INDIRETTO)
    @patch.object(GPIO, "input")
    def test_check_number_occupied_spots(self, mock_distance_sensor: Mock):
        mock_distance_sensor.side_effect = [True, False, True] # Mock dell'uso di GPIO.input tre volte. Per dare un array di risultati diversi ogni chiamata va usato side_effect, return_value va bene solo per un valore costante.
        system = ParkingGarage()
        num = system.get_number_occupied_spots()
        self.assertEqual(num, 2)

    # ESEMPIO DI TEST STUB (Replacement di INPUT INDIRETTO)
    @patch.object(SDL_DS3231, "read_datetime") # Si potrebbe usare anche @patch("SDL_DS3231.read_datetime") qui così come negli altri casi, ma "patch" è di solito usato per funzioni contenute all'interno di moduli.
    def test_parking_fee_regular_days(self, mock_time_sensor: Mock):
        mock_time_sensor.return_value = datetime(2024, 11, 11, 15, 45)
        system = ParkingGarage()
        cost = system.calculate_parking_fee(datetime(2024, 11, 11, 12, 00))
        self.assertEqual(cost, 10)

    # ESEMPIO DI TEST STUB (Replacement di INPUT INDIRETTO)
    @patch.object(SDL_DS3231, "read_datetime")
    def test_parking_fee_weekend_days(self, mock_time_sensor: Mock):
        mock_time_sensor.return_value = datetime(2024, 11, 10, 15, 45)
        system = ParkingGarage()
        cost = system.calculate_parking_fee(datetime(2024, 11, 10, 12, 00))
        self.assertEqual(cost, 12.5)

    # ESEMPIO DI MOCK OBJECT (Analisi e asserzione su OUTPUT INDIRETTO), non TEST SPY in quanto questo si occupa solamente di osservare
    @patch.object(ParkingGarage, "change_servo_angle")
    def test_open_garage_door(self, mock_servo: Mock):
        system = ParkingGarage()
        system.open_garage_door()
        mock_servo.assert_called_with(12) # Controlla che il metodo change_servo_angle venga usato con argomento "12". Genera assertionerror se non succede!
        self.assertTrue(system.open_garage_door) # Questo qui da sempre true se il metodo esiste

    # ESEMPIO DI MOCK OBJECT (Analisi e asserzione su OUTPUT INDIRETTO), non TEST SPY in quanto questo si occupa solamente di osservare
    @patch.object(ParkingGarage, "change_servo_angle")
    def test_closed_garage_door(self, mock_servo: Mock):
        system = ParkingGarage()
        system.close_garage_door()
        mock_servo.assert_called_with(0)  # Controlla che il metodo change_servo_angle venga usato con argomento "12". Genera assertionerror se non succede!
        self.assertTrue(system.close_garage_door)  # Questo qui da sempre true se il metodo esiste

    @patch.object(ParkingGarage, "change_servo_angle")  # Questo è un TEST SPY (Osservazione di OUTPUT INDIRETTO)
    def test_closed_garage_door_spy(self, mock_servo: Mock):
        system = ParkingGarage()
        system.close_garage_door()
        # Il Test Spy si limita a osservare senza fare asserzioni attive né influenza input indiretti.
        calls = mock_servo.call_args_list  # Osserva le chiamate effettuate
        print(f"Calls made to change_servo_angle: {calls}")  # Output solo per osservazione
        self.assertTrue(
            len(calls) > 0)  # Verifica che almeno una chiamata è stata fatta (opzionale, non verifica gli argomenti esatti)

    # Osservazione di output diretto
    def test_red_light_on(self):
        system = ParkingGarage()
        system.turn_on_red_light()
        self.assertTrue(system.red_light_on)

    # Input e output diretti qui
    def test_red_light_off(self):
        system = ParkingGarage()
        system.red_light_on = True
        system.turn_off_red_light()
        self.assertTrue(not system.red_light_on)

    #L'ordine degli assegnamenti agli oggetti di mock in argomento è all'inverso rispetto ai decoratori (dal basso il primo, verso l'alto gli altri)
    @patch.object(ParkingGarage, "turn_off_red_light") # Questo è un MOCK OBJECT (Analisi e asserzione su OUTPUT INDIRETTO)
    @patch.object(GPIO, "input") # Questo è un TEST STUB (inietta INPUT INDIRETTI)
    def test_manage_red_light_when_not_full(self, mock_distance_sensor: Mock, mock_parking_garage: Mock):
        mock_distance_sensor.side_effect = [True, False, True]
        system = ParkingGarage()
        system.manage_red_light()
        mock_parking_garage.assert_called()
        self.assertTrue(system.manage_red_light)

    @patch.object(ParkingGarage, "turn_off_red_light")  # Questo è un MOCK OBJECT (Analisi e asserzione su OUTPUT INDIRETTO)
    @patch.object(GPIO, "input")  # Questo è un TEST STUB (inietta INPUT INDIRETTI)
    def test_manage_red_light_when_full(self, mock_distance_sensor: Mock, mock_parking_garage: Mock):
        mock_distance_sensor.side_effect = [True, True, True]
        system = ParkingGarage()
        system.manage_red_light()
        mock_parking_garage.assert_called()
        self.assertTrue(system.manage_red_light)