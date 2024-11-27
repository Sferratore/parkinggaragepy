from datetime import datetime
# Mock library for https://github.com/switchdoclabs/RTC_SDL_DS3231. This is a FAKE OBJECT too.

class SDL_DS3231:

    def __init__(self, twi=1, addr=0x68, at24c32_addr=0x56):
        pass

    def read_datetime(self):
        """Return the datetime.datetime object."""
        return datetime.now()