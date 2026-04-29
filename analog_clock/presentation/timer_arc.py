import tkinter as tk

class TimerArc(tk.Canvas):
    def __init__(self, parent, bg_color="#FFEDD5", **kwargs):
        super().__init__(parent, bg=bg_color, highlightthickness=0, **kwargs)
        self.width = kwargs.get("width", 200)
        self.height = kwargs.get("height", 200)
        self.accent_color = "#FF6B6B"
        
    def draw_base_ring(self):
        self.delete("all")
        margin = 10
        self.create_oval(margin, margin, self.width-margin, self.height-margin, outline="#E0D0B8", width=10)

    def update_progress(self, ratio: float):
        self.draw_base_ring()
        extent = -(ratio * 359.99) # negative for clockwise
        margin = 10
        self.create_arc(margin, margin, self.width-margin, self.height-margin, start=90, extent=extent, style=tk.ARC, outline=self.accent_color, width=10)

