import math
import tkinter as tk
from domain.clock_state import ClockState

class HandRenderer:
    def __init__(self, canvas: tk.Canvas, clock_state: ClockState):
        self.canvas = canvas
        self.clock_state = clock_state
        self.center_x = float(canvas.cget("width")) / 2
        self.center_y = float(canvas.cget("height")) / 2
        self.radius = min(self.center_x, self.center_y) - 15
        self.hand_ids = []
        
        self.is_dragging = False
        self.dragged_hand = None
        self.old_m = 0
        self.old_s = 0
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        h, m, s = self.clock_state.get_time()
        dx = event.x - self.center_x
        dy = event.y - self.center_y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 10: return # ignore center clicks
        
        angle = (math.degrees(math.atan2(dy, dx)) + 90) % 360
        
        h_angle = ((h % 12 + m / 60) * 30) % 360
        m_angle = ((m + s / 60) * 6) % 360
        s_angle = (s * 6) % 360
        
        def angle_diff(a1, a2):
            diff = abs(a1 - a2)
            return min(diff, 360 - diff)
            
        tolerance = 20
        
        if dist < self.radius * 0.95 and dist > self.radius * 0.4:
            if angle_diff(angle, s_angle) < tolerance:
                self.dragged_hand = "second"
                self.is_dragging = True
                self.old_s = s
            elif angle_diff(angle, m_angle) < tolerance:
                self.dragged_hand = "minute"
                self.is_dragging = True
                self.old_m = m
        if not self.is_dragging and dist < self.radius * 0.6:
            if angle_diff(angle, h_angle) < tolerance:
                self.dragged_hand = "hour"
                self.is_dragging = True

    def on_motion(self, event):
        if not self.is_dragging: return
        
        dx = event.x - self.center_x
        dy = event.y - self.center_y
        angle = (math.degrees(math.atan2(dy, dx)) + 90) % 360
        
        h, m, s = self.clock_state.get_time()
        
        if self.dragged_hand == "hour":
            new_h = int(angle / 30)
            if h >= 12: new_h += 12 # preserve PM
            self.clock_state.set_time(new_h, m, s)
        elif self.dragged_hand == "minute":
            new_m = int(angle / 6)
            
            if self.old_m > 45 and new_m < 15:
                h = (h + 1) % 24
            elif self.old_m < 15 and new_m > 45:
                h = (h - 1) % 24
                
            self.old_m = new_m
            self.clock_state.set_time(h, new_m, s)
        elif self.dragged_hand == "second":
            new_s = int(angle / 6)
            
            if self.old_s > 45 and new_s < 15:
                m = (m + 1) % 60
                if m == 0:
                    h = (h + 1) % 24
            elif self.old_s < 15 and new_s > 45:
                m = (m - 1) % 60
                if m == 59:
                    h = (h - 1) % 24
                    
            self.old_s = new_s
            self.clock_state.set_time(h, m, new_s)
            
        self.draw_hands()
        
    def on_release(self, event):
        self.is_dragging = False
        self.dragged_hand = None

    def draw_hands(self):
        for id in self.hand_ids:
            self.canvas.delete(id)
        self.hand_ids.clear()
        
        h, m, s = self.clock_state.get_time()
        
        h_angle = math.radians((h % 12 + m / 60) * 30 - 90)
        m_angle = math.radians((m + s / 60) * 6 - 90)
        s_angle = math.radians(s * 6 - 90)
        
        hx = self.center_x + (self.radius * 0.5) * math.cos(h_angle)
        hy = self.center_y + (self.radius * 0.5) * math.sin(h_angle)
        self.hand_ids.append(self.canvas.create_line(self.center_x, self.center_y, hx, hy, width=6, fill="#333"))

        mx = self.center_x + (self.radius * 0.75) * math.cos(m_angle)
        my = self.center_y + (self.radius * 0.75) * math.sin(m_angle)
        self.hand_ids.append(self.canvas.create_line(self.center_x, self.center_y, mx, my, width=4, fill="#58A6FF"))

        sx = self.center_x + (self.radius * 0.9) * math.cos(s_angle)
        sy = self.center_y + (self.radius * 0.9) * math.sin(s_angle)
        self.hand_ids.append(self.canvas.create_line(self.center_x, self.center_y, sx, sy, width=2, fill="#FF6B6B"))

        self.hand_ids.append(self.canvas.create_oval(self.center_x - 5, self.center_y - 5, self.center_x + 5, self.center_y + 5, fill="#333"))

