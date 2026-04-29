from domain.pomodoro_routine import PomodoroRoutine
from .sound_emitter import SoundEmitter

class PomodoroTracker:
    def __init__(self, routine: PomodoroRoutine, audio_system: SoundEmitter):
        self.routine = routine
        self.audio_system = audio_system
        self.is_active = False

    def start(self):
        self.is_active = True

    def pause(self):
        self.is_active = False
        
    def skip_phase(self):
        """Uses 'next' pointer functionality of Domain."""
        self.routine.advance_to_next()
        
    def restart_phase(self):
        """Uses 'previous' pointer functionality of Domain."""
        self.routine.restart_current()

    def tick(self):
        """Ticks the domain clock down, handles sounds if finished."""
        if not self.is_active:
            return
            
        finished = self.routine.tick_down()
        if finished:
            self.audio_system.emit_session_end_beep()
            self.routine.advance_to_next()
