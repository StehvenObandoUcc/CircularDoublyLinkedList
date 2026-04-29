import tkinter as tk
from logic.pomodoro_tracker import PomodoroTracker
from .timer_arc import TimerArc

class PomodoroPanel(tk.Frame):
    def __init__(self, parent, tracker: PomodoroTracker, bg_color="#FFEDD5"):
        super().__init__(parent, bg=bg_color)
        self.tracker = tracker
        self.bg_color = bg_color
        self.build_interface()

    def build_interface(self):
        container = tk.LabelFrame(self, text="Pomodoro", font=("Helvetica", 10, "bold"), bg=self.bg_color, fg="#333", bd=0)
        container.pack(fill=tk.X, padx=10, pady=5)
        
        self.timer_arc = TimerArc(container, bg_color=self.bg_color, width=150, height=150)
        self.timer_arc.pack(pady=10)
        
        self.lbl_phase = tk.Label(container, text="Pomodoro", font=("Helvetica", 14, "bold"), bg=self.bg_color, fg="#333")
        self.lbl_phase.pack()
        
        self.lbl_time = tk.Label(container, text="00:00", font=("Helvetica", 28, "bold"), bg=self.bg_color, fg="#FF3B30")
        self.lbl_time.pack(pady=5)
        
        btn_frame = tk.Frame(container, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        btn_style_primary = {"bg": "#007AFF", "fg": "white", "bd": 0, "font": ("Helvetica", 10, "bold"), "padx": 15, "pady": 6, "activebackground": "#0056b3", "activeforeground": "white"}
        btn_style_secondary = {"bg": "#E5E5EA", "fg": "#007AFF", "bd": 0, "font": ("Helvetica", 10, "bold"), "padx": 15, "pady": 6, "activebackground": "#D1D1D6"}
        btn_style_destructive = {"bg": "#FF3B30", "fg": "white", "bd": 0, "font": ("Helvetica", 10, "bold"), "padx": 15, "pady": 6, "activebackground": "#c92a22", "activeforeground": "white"}
        
        tk.Button(btn_frame, text="Start", command=self.tracker.start, **btn_style_primary).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Pause", command=self.tracker.pause, **btn_style_secondary).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Skip", command=self.tracker.skip_phase, **btn_style_destructive).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Restart", command=self.tracker.restart_phase, **btn_style_secondary).pack(side=tk.LEFT, padx=5)

    def refresh_display(self):
        if self.tracker.routine.active_phase:
            phase = self.tracker.routine.active_phase
            rem = self.tracker.routine.remaining_seconds
            
            self.lbl_phase.config(text=phase.label)
            self.lbl_time.config(text=f"{rem // 60:02d}:{rem % 60:02d}")
            self.timer_arc.update_progress(self.tracker.routine.get_progress_ratio())


