import tkinter as tk
from logic.alarm_scheduler import AlarmScheduler
from logic.time_advancer import TimeAdvancer

class AlarmPanel(tk.Frame):
    def __init__(self, parent, scheduler: AlarmScheduler, advancer: TimeAdvancer, bg_color="#FFEDD5"):
        super().__init__(parent, bg=bg_color)
        self.scheduler = scheduler
        self.advancer = advancer
        self.bg_color = bg_color
        self.build_interface()

    def build_interface(self):
        alarm_frame = tk.LabelFrame(self, text="Alarm Config", bg=self.bg_color, fg="#333", font=("Helvetica", 10, "bold"), bd=0)
        alarm_frame.pack(fill=tk.X, padx=10, pady=5)
        
        time_frame = tk.Frame(alarm_frame, bg=self.bg_color)
        time_frame.pack(pady=5)
        
        self.h_var = tk.StringVar(value="12")
        self.m_var = tk.StringVar(value="00")
        self.ampm_var = tk.StringVar(value="AM")
        
        entry_bg = "#FFFFFF"
        tk.Entry(time_frame, textvariable=self.h_var, width=3, bg=entry_bg, relief=tk.FLAT, font=("Helvetica", 12)).pack(side=tk.LEFT)
        tk.Label(time_frame, text=":", bg=self.bg_color, font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)
        tk.Entry(time_frame, textvariable=self.m_var, width=3, bg=entry_bg, relief=tk.FLAT, font=("Helvetica", 12)).pack(side=tk.LEFT)
        
        opt = tk.OptionMenu(time_frame, self.ampm_var, "AM", "PM")
        opt.config(bg=entry_bg, relief=tk.FLAT, activebackground="#F2F2F7", highlightthickness=0)
        opt.pack(side=tk.LEFT, padx=5)
        
        btn_frame = tk.Frame(alarm_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        btn_style_primary = {"bg": "#007AFF", "fg": "white", "bd": 0, "font": ("Helvetica", 10, "bold"), "padx": 15, "pady": 6, "activebackground": "#0056b3", "activeforeground": "white"}
        btn_style_secondary = {"bg": "#E5E5EA", "fg": "#007AFF", "bd": 0, "font": ("Helvetica", 10, "bold"), "padx": 15, "pady": 6, "activebackground": "#D1D1D6"}
        btn_style_destructive = {"bg": "#FF3B30", "fg": "white", "bd": 0, "font": ("Helvetica", 10, "bold"), "padx": 15, "pady": 6, "activebackground": "#c92a22", "activeforeground": "white"}
        
        tk.Button(btn_frame, text="Set", command=self.set_alarm, **btn_style_primary).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Off", command=self.disable_alarm, **btn_style_secondary).pack(side=tk.LEFT, padx=5)
        
        self.status_lbl = tk.Label(alarm_frame, text="Alarm: Off", bg=self.bg_color, fg="#8E8E93", font=("Helvetica", 10))
        self.status_lbl.pack(pady=5)
        
        custom_frame = tk.LabelFrame(self, text="Clock Settings", bg=self.bg_color, fg="#333", font=("Helvetica", 10, "bold"), bd=0)
        custom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        c_time_frame = tk.Frame(custom_frame, bg=self.bg_color)
        c_time_frame.pack(pady=5)
        
        self.ch_var = tk.StringVar(value="12")
        self.cm_var = tk.StringVar(value="00")
        self.cs_var = tk.StringVar(value="00")
        self.campm_var = tk.StringVar(value="PM")
        
        tk.Entry(c_time_frame, textvariable=self.ch_var, width=3, bg=entry_bg, relief=tk.FLAT, font=("Helvetica", 12)).pack(side=tk.LEFT)
        tk.Label(c_time_frame, text=":", bg=self.bg_color, font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)
        tk.Entry(c_time_frame, textvariable=self.cm_var, width=3, bg=entry_bg, relief=tk.FLAT, font=("Helvetica", 12)).pack(side=tk.LEFT)
        tk.Label(c_time_frame, text=":", bg=self.bg_color, font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)
        tk.Entry(c_time_frame, textvariable=self.cs_var, width=3, bg=entry_bg, relief=tk.FLAT, font=("Helvetica", 12)).pack(side=tk.LEFT)
        
        c_opt = tk.OptionMenu(c_time_frame, self.campm_var, "AM", "PM")
        c_opt.config(bg=entry_bg, relief=tk.FLAT, activebackground="#F2F2F7", highlightthickness=0)
        c_opt.pack(side=tk.LEFT, padx=5)
        
        c_btn_frame = tk.Frame(custom_frame, bg=self.bg_color)
        c_btn_frame.pack(pady=10)
        
        tk.Button(c_btn_frame, text="Apply Custom Time", command=self.set_custom_time, **btn_style_primary).pack(side=tk.LEFT, padx=5)
        tk.Button(c_btn_frame, text="Apply Local Time", command=self.advancer.sync_to_system_time, **btn_style_secondary).pack(side=tk.LEFT, padx=5)

    def set_alarm(self):
        try:
            h = int(self.h_var.get())
            m = int(self.m_var.get())
            
            if self.ampm_var.get() == "PM" and h != 12:
                h += 12
            elif self.ampm_var.get() == "AM" and h == 12:
                h = 0
                
            self.scheduler.set_alarm(h, m)
            self.status_lbl.config(text=f"Alarm: {self.scheduler.get_alarm_string()}")
        except ValueError:
            pass

    def disable_alarm(self):
        self.scheduler.disable_alarm()
        self.status_lbl.config(text="Alarm: Off")
        
    def set_custom_time(self):
        try:
            h = int(self.ch_var.get())
            m = int(self.cm_var.get())
            s = int(self.cs_var.get())
            
            if self.campm_var.get() == "PM" and h != 12:
                h += 12
            elif self.campm_var.get() == "AM" and h == 12:
                h = 0
                
            self.advancer.set_custom_time(h, m, s)
        except ValueError:
            pass


