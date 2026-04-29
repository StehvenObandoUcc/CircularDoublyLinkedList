import sys
import os
import time
import threading

class SoundEmitter:
    """
    Cross-platform abstraction for sound emission without third-party libraries.
    """
    def __init__(self):
        self._stop_alarm_flag = False

    def _play(self, frequency: int, duration_ms: int):
        if sys.platform == "win32":
            import winsound
            if frequency > 37: # winsound.Beep minimum is 37
                winsound.Beep(frequency, duration_ms)
            elif frequency == 0:
                time.sleep(duration_ms / 1000.0)
            else:
                # System fallback
                winsound.MessageBeep(-1) 
        else:
            # Fallback for unix like
            if frequency > 0:
                os.system(f"play -nq -t alsa synth {duration_ms/1000.0} sine {frequency} 2>/dev/null")
            else:
                time.sleep(duration_ms / 1000.0)

    def _async_alarm(self):
        self._stop_alarm_flag = False
        for _ in range(120): # Loop up to 120 times (around 1 minute)
            if self._stop_alarm_flag:
                break
            self._play(800, 300)
            if self._stop_alarm_flag:
                break
            self._play(0, 200) # pause between beeps

    def stop_alarm(self):
        self._stop_alarm_flag = True

    def emit_alarm_beep(self):
        # Run in a separate thread to prevent freezing the UI
        threading.Thread(target=self._async_alarm, daemon=True).start()
            
    def _async_session(self):
        self._play(600, 800)

    def emit_session_end_beep(self):
        # Run in a separate thread to prevent freezing the UI
        threading.Thread(target=self._async_session, daemon=True).start()
