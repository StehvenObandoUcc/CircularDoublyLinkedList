from .pomodoro_phase import PomodoroPhase

class PomodoroRoutine:
    """
    Doubly Circular Linked List managing Pomodoro phases sequentially.
    """
    def __init__(self):
        self.active_phase = None
        self.remaining_seconds = 0

    def add_phase(self, label: str, duration_seconds: int):
        """Inserts at end."""
        new_phase = PomodoroPhase(label, duration_seconds)
        
        if self.active_phase is None:
            self.active_phase = new_phase
            new_phase.next_phase = self.active_phase
            new_phase.previous_phase = self.active_phase
        else:
            last_phase = self.active_phase.previous_phase
            
            last_phase.next_phase = new_phase
            new_phase.next_phase = self.active_phase
            
            new_phase.previous_phase = last_phase
            self.active_phase.previous_phase = new_phase

    def build_standard_routine(self):
        """Constructs an infinite cycle Pomodoro: 4 Work, 3 Short Break, 1 Long Break."""
        work_duration = 25 * 60
        short_break = 5 * 60
        long_break = 15 * 60

        self.add_phase("Work", work_duration)
        self.add_phase("Short Break", short_break)
        self.add_phase("Work", work_duration)
        self.add_phase("Short Break", short_break)
        self.add_phase("Work", work_duration)
        self.add_phase("Short Break", short_break)
        self.add_phase("Work", work_duration)
        self.add_phase("Long Break", long_break)
        
        # Initialize the timer with the first active phase
        if self.active_phase:
            self.remaining_seconds = self.active_phase.duration_seconds

    def advance_to_next(self):
        """Jumps to the next phase and resets its clock."""
        if self.active_phase is not None:
            self.active_phase = self.active_phase.next_phase
            self.remaining_seconds = self.active_phase.duration_seconds

    def restart_current(self):
        """Resets the current phase to its full duration, logically doing a 'previous' jump to reevaluate node."""
        if self.active_phase is not None:
            previous = self.active_phase.previous_phase
            self.active_phase = previous.next_phase
            self.remaining_seconds = self.active_phase.duration_seconds

    def tick_down(self) -> bool:
        """
        Decrements internal timer.
        Returns True if the phase just finished (hit 0).
        """
        if self.active_phase is None or self.remaining_seconds <= 0:
            return False
            
        self.remaining_seconds -= 1
        
        if self.remaining_seconds <= 0:
            return True
            
        return False

    def get_progress_ratio(self) -> float:
        """Returns 0.0 to 1.0 representing phase progression."""
        if self.active_phase is None or self.active_phase.duration_seconds == 0:
            return 0.0
        elapsed = self.active_phase.duration_seconds - self.remaining_seconds
        return elapsed / self.active_phase.duration_seconds
