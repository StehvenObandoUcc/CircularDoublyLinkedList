from domain.clock_state import ClockState
from .sound_emitter import SoundEmitter

class AlarmScheduler:
    def __init__(self, clock_state: ClockState, sound_emitter: SoundEmitter):
        self.clock_state = clock_state
        self.sound_emitter = sound_emitter
        self.is_active = False
        self.target_hours = 0
        self.target_minutes = 0
        self.has_rung = False

    def disable_alarm(self):
        self.is_active = False
        self.sound_emitter.stop_alarm()
        
    def set_alarm(self, h: int, m: int):
        self.target_hours = h
        self.target_minutes = m
        self.is_active = True
        self.has_rung = False

    def get_alarm_string(self) -> str:
        if not self.is_active:
            return "Off"
        return f"{self.target_hours:02d}:{self.target_minutes:02d}"

    def evaluate(self):
        if not self.is_active or self.has_rung:
            return
            
        current_h, current_m, current_s = self.clock_state.get_time()
        
        # Trigger when hours and minutes match. 
        # We check has_rung to ensure it doesn't trigger multiple times in the same minute.
        if current_h == self.target_hours and current_m == self.target_minutes:
            self.sound_emitter.emit_alarm_beep()
            self.has_rung = True
        
    def reset_alarm_status_if_needed(self):
        """Resets has_rung if the time has moved away from the target minute."""
        current_h, current_m, _ = self.clock_state.get_time()
        if self.has_rung and (current_h != self.target_hours or current_m != self.target_minutes):
            self.has_rung = False
