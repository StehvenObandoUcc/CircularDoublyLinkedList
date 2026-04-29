import datetime
from domain.clock_state import ClockState

class TimeAdvancer:
    def __init__(self, clock_state: ClockState):
        self.clock_state = clock_state

    def sync_to_system_time(self):
        now = datetime.datetime.now()
        self.clock_state.set_time(now.hour, now.minute, now.second)
    
    def set_custom_time(self, hours: int, minutes: int, seconds: int):
        self.clock_state.set_time(hours, minutes, seconds)

    def tick(self):
        """Advances the internal clock state by 1 second."""
        self.clock_state.tick_second()
