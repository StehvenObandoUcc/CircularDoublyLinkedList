from .dial_ring import DialRing

class ClockState:
    """
    Maintains the state of hours, minutes, and seconds, each governed by a DialRing.
    """
    def __init__(self):
        self.hours_ring = DialRing()
        self.minutes_ring = DialRing()
        self.seconds_ring = DialRing()

        self.hours_ring.build_ring(24) # Internal clock is 24 hours format
        self.minutes_ring.build_ring(60)
        self.seconds_ring.build_ring(60)

    def set_time(self, hours: int, minutes: int, seconds: int):
        """Sets the active node for each ring."""
        self.hours_ring.set_current_value(hours % 24)
        self.minutes_ring.set_current_value(minutes % 60)
        self.seconds_ring.set_current_value(seconds % 60)

    def tick_second(self):
        """Advances the seconds ring, bubbling up to minutes and hours on overflow."""
        self.seconds_ring.advance_to_next()
        if self.seconds_ring.get_current_value() == 0:
            self.minutes_ring.advance_to_next()
            if self.minutes_ring.get_current_value() == 0:
                self.hours_ring.advance_to_next()

    def get_time(self):
        """Returns the current components (hours, minutes, seconds)."""
        return (
            self.hours_ring.get_current_value(),
            self.minutes_ring.get_current_value(),
            self.seconds_ring.get_current_value()
        )
