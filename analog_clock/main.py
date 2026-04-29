import tkinter as tk
from domain import ClockState, PomodoroRoutine
from logic import TimeAdvancer, AlarmScheduler, SoundEmitter, PomodoroTracker
from presentation import PomodoroPanel, ClockFace, HandRenderer, AlarmPanel

class AnalogClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taller Reloj / Pomodoro")
        self.root.geometry("800x650")
        self.root.configure(bg="#FFEDD5")
        
        # --- DOMAIN INIT ---
        self.clock_state = ClockState()
        self.pomodoro_routine = PomodoroRoutine()
        self.pomodoro_routine.build_standard_routine()
        
        # --- LOGIC INIT ---
        self.sound_emitter = SoundEmitter()
        self.time_advancer = TimeAdvancer(self.clock_state)
        self.time_advancer.sync_to_system_time()
        
        self.alarm_scheduler = AlarmScheduler(self.clock_state, self.sound_emitter)
        self.pomodoro_tracker = PomodoroTracker(self.pomodoro_routine, self.sound_emitter)
        
        # --- PRESENTATION INIT ---
        main_frame = tk.Frame(self.root, bg="#FFEDD5")
        main_frame.pack(expand=True) # Centered main frame without filling everything
        
        content_frame = tk.Frame(main_frame, bg="#FFEDD5")
        content_frame.pack(padx=20, pady=20)
        
        # Panel Izquierdo (Reloj y Alarma)
        left_panel = tk.Frame(content_frame, bg="#FFEDD5")
        left_panel.pack(side=tk.LEFT, padx=20)
        
        clock_title = tk.Label(left_panel, text="Reloj", bg="#FFEDD5", fg="#333", font=("Helvetica", 10, "bold"))
        clock_title.pack(anchor="w", padx=10)
        
        self.clock_face = ClockFace(left_panel, width=300, height=300)
        self.clock_face.pack(pady=10)
        self.hand_renderer = HandRenderer(self.clock_face, self.clock_state)
        
        self.alarm_panel = AlarmPanel(left_panel, self.alarm_scheduler, self.time_advancer)
        self.alarm_panel.pack(fill=tk.X, pady=10)
        
        # Panel Derecho (Pomodoro)
        right_panel = tk.Frame(content_frame, bg="#FFEDD5")
        right_panel.pack(side=tk.RIGHT, padx=20)
        
        self.pomodoro_panel = PomodoroPanel(right_panel, self.pomodoro_tracker)
        self.pomodoro_panel.pack(pady=20)
        
        # Iniciar ciclo de interfaz
        self.root.after(10, self.hand_renderer.draw_hands)
        self.root.after(1000, self.main_loop)

    def main_loop(self):
        # 1. Update Analog Clock State
        if not self.hand_renderer.is_dragging:
            self.time_advancer.tick()
            
        self.hand_renderer.draw_hands()
        
        # 2. Evaluate Alarm
        self.alarm_scheduler.evaluate()
        self.alarm_scheduler.reset_alarm_status_if_needed()
        
        # 3. Update Pomodoro State
        self.pomodoro_tracker.tick()
        self.pomodoro_panel.refresh_display()
        
        # 4. Recursion
        self.root.after(1000, self.main_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalogClockApp(root)
    root.mainloop()

