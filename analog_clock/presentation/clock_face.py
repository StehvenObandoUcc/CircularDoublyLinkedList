import tkinter as tk
import math

class ClockFace(tk.Canvas):
    def __init__(self, parent, bg_color="#FFEDD5", **kwargs):
        super().__init__(parent, bg=bg_color, highlightthickness=0, **kwargs)
        self.width = kwargs.get("width", 300)
        self.height = kwargs.get("height", 300)
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.radius = min(self.center_x, self.center_y) - 15
        
        self.draw_face()

    def draw_face(self):
        self.create_oval(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            fill="white", outline="#58A6FF", width=4
        )
        roman_nums = ["XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x1 = self.center_x + (self.radius - 10) * math.cos(angle)
            y1 = self.center_y + (self.radius - 10) * math.sin(angle)
            x2 = self.center_x + self.radius * math.cos(angle)
            y2 = self.center_y + self.radius * math.sin(angle)
            self.create_line(x1, y1, x2, y2, fill="#58A6FF", width=3)
            
            # Numeric labels
            text_x = self.center_x + (self.radius - 30) * math.cos(angle)
            text_y = self.center_y + (self.radius - 30) * math.sin(angle)
            self.create_text(text_x, text_y, text=roman_nums[i], fill="#58A6FF", font=("Helvetica", 14, "bold"))
            
        self.create_oval(self.center_x - 5, self.center_y - 5, self.center_x + 5, self.center_y + 5, fill="#333")

