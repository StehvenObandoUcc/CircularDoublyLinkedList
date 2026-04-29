class PomodoroPhase:
    """
    Node representing a specific block of time in a Pomodoro routine.
    """
    def __init__(self, label: str, duration_seconds: int):
        self.label = label
        self.duration_seconds = duration_seconds
        
        # Bidirectional pointers
        self.next_phase = None
        self.previous_phase = None

    def __repr__(self):
        return f"PomodoroPhase({self.label}, {self.duration_seconds}s)"
