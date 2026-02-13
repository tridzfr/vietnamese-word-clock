import tkinter as tk
from tkinter import ttk
import math
import datetime
import json
import os

THEMES = {
    "Tiêu chuẩn": {"bg": "#121212", "grid_dim": "#1f1f1f", "ui_dim": "#333333", "lit": "#ffffff", "accent": "#00d2ff", "sec": "#ff3b30"},
    "Huyền bí":   {"bg": "#282a36", "grid_dim": "#343746", "ui_dim": "#44475a", "lit": "#f8f8f2", "accent": "#bd93f9", "sec": "#ff79c6"},
    "Neon":       {"bg": "#0b0c15", "grid_dim": "#151726", "ui_dim": "#22263d", "lit": "#ff2a6d", "accent": "#05d9e8", "sec": "#d1f7ff"},
    "Rừng xanh":  {"bg": "#021a0c", "grid_dim": "#052612", "ui_dim": "#0a4020", "lit": "#98fb98", "accent": "#00ff7f", "sec": "#ffffff"},
    "Biển sâu":   {"bg": "#001e26", "grid_dim": "#012d38", "ui_dim": "#034d5e", "lit": "#e0f7fa", "accent": "#00bcd4", "sec": "#ff9800"},
    "Tối giản":   {"bg": "#000000", "grid_dim": "#1a1a1a", "ui_dim": "#333333", "lit": "#eeeeee", "accent": "#ffffff", "sec": "#ffffff"},
    "Chiều tà":   {"bg": "#2d1b2e", "grid_dim": "#3d243e", "ui_dim": "#5c3b3e", "lit": "#ffd700", "accent": "#ff6b6b", "sec": "#feca57"},
    "Anh đào":    {"bg": "#2d142c", "grid_dim": "#3d1d3b", "ui_dim": "#5e2a5a", "lit": "#fff0f5", "accent": "#ff8fab", "sec": "#ffb3c1"},
    "Sa mạc":     {"bg": "#2b1d0e", "grid_dim": "#3d2b18", "ui_dim": "#5e452a", "lit": "#fef5e7", "accent": "#edae49", "sec": "#d1495b"},
    "Băng giá":   {"bg": "#0f172a", "grid_dim": "#1e293b", "ui_dim": "#334155", "lit": "#f1f5f9", "accent": "#38bdf8", "sec": "#94a3b8"},
    "Cổ điển":    {"bg": "#2c2c2c", "grid_dim": "#3d3d3d", "ui_dim": "#4a4a4a", "lit": "#dcdcdc", "accent": "#c5a059", "sec": "#8b0000"},
}

GRID_CHARS = [
    ['b', 'â', 'y', 'm', 'g', 'i', 'ờ', 't', 'l', 'à'],
    ['m', 'ư', 'ờ', 'i', 'b', 'ả', 'y', 'h', 'a', 'i'],
    ['c', 'h', 'í', 'n', 'ă', 'm', 'ộ', 't', 'á', 'm'],
    ['s', 'á', 'u', 'b', 'ố', 'n', 'r', 'g', 'i', 'ờ'],
    ['k', 'é', 'm', 'r', 'ư', 'ỡ', 'i', 'h', 'a', 'i'],
    ['n', 'ă', 'm', 'ư', 'ờ', 'i', 'í', 'l', 'ă', 'm'],
]

DAYS_VN = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
def get_range(r, c1, c2): return [(r, c) for c in range(c1, c2 + 1)]

WORDS = {
    "PREFIX":   get_range(0, 0, 2) + get_range(0, 4, 6) + get_range(0, 8, 9),
    "HOURS_1":  get_range(2, 5, 7), "HOURS_2":  get_range(1, 7, 9),
    "HOURS_3":  get_range(1, 4, 5), "HOURS_4":  get_range(3, 3, 5),
    "HOURS_5":  get_range(2, 3, 5), "HOURS_6":  get_range(3, 0, 2),
    "HOURS_7":  get_range(1, 4, 6), "HOURS_8":  get_range(2, 7, 9),
    "HOURS_9":  get_range(2, 0, 3), "HOURS_10": get_range(1, 0, 3),
    "HOURS_11": get_range(1, 0, 3) + get_range(2, 5, 7),
    "HOURS_12": get_range(1, 0, 3) + get_range(1, 7, 9),
    "GIO":       get_range(3, 7, 9), "KEM":      get_range(4, 0, 2),
    "RUOI":     get_range(4, 3, 6), "MIN_5":    get_range(5, 0, 2),
    "MIN_10":   get_range(5, 2, 5), "MIN_TY":   get_range(5, 2, 5),
    "MIN_LAM":  get_range(5, 7, 9), "MIN_2":    get_range(4, 7, 9),
}

MINUTE_PATTERNS = {
    0: [], 5: ["MIN_5"], 10: ["MIN_10"], 15: ["MIN_10", "MIN_LAM"],
    20: ["MIN_2", "MIN_TY"], 25: ["MIN_2", "MIN_TY", "MIN_LAM"], 30: ["RUOI"]
}

OVERRIDES = {"HOURS_3": {(1, 5): "a"}, "MIN_TY": {(5, 4): "ơ"}}

class StudioClock(tk.Tk):
    NORM_W, NORM_H = 960, 600
    MINI_W, MINI_H = 450, 350 
    TOOLBAR_H = 35

    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        conf = self.load_config()
        self.theme_name = conf.get("theme", "Tiêu chuẩn")
        self.is_mini = conf.get("is_mini", False)
        self.offset_seconds = conf.get("offset_seconds", 0)
        pos_x = conf.get("x", 200)
        pos_y = conf.get("y", 200)
        cur_w, cur_h = (self.MINI_W, self.MINI_H) if self.is_mini else (self.NORM_W, self.NORM_H)
        self.geometry(f"{cur_w}x{cur_h}+{pos_x}+{pos_y}")
        self.t = THEMES.get(self.theme_name, THEMES["Tiêu chuẩn"]).copy()
        self.show_settings = False
        self.test_mode, self.test_val = False, 0
        self.active_chars_prev = {}
        self.toast_after_id = None 
        self.text_ids = {}
        self.configure(bg=self.t["bg"])
        self.attributes("-topmost", True)
        self.content_frame = tk.Frame(self, bg=self.t["bg"])
        self.content_frame.pack(side="top", fill="both", expand=True)
        self.icon_bar = tk.Frame(self, bg=self.t["bg"])
        self.toolbar = tk.Frame(self, bg=self.t["ui_dim"], height=self.TOOLBAR_H)
        self.greeting = tk.Label(self.content_frame, text="", fg=self.t["accent"], bg=self.t["bg"], font=("Courier New", 22, "bold"))
        self.main_container = tk.Frame(self.content_frame, bg=self.t["bg"])
        self.main_container.pack(side="top", expand=True, fill="both", padx=40)
        self.toast_lbl = tk.Label(self.content_frame, text="", bg=self.t["bg"], font=("Courier New", 14, "bold"), anchor="w")
        self.toast_lbl.place(x=20, y=15, anchor="nw")
        self.word_canvas = tk.Canvas(self.main_container, width=540, height=360, bg=self.t["bg"], highlightthickness=0)
        self.word_canvas.pack(side="left")
        self.right_stack = tk.Frame(self.main_container, bg=self.t["bg"], width=280)
        self.right_stack.pack(side="left", fill="y", padx=(50, 0))
        self.right_stack.pack_propagate(False)
        self.analog = tk.Canvas(self.right_stack, width=240, height=240, bg=self.t["bg"], highlightthickness=0)
        self.analog.pack(side="top", pady=(80, 0))
        self.digital_lbl = tk.Label(self.right_stack, text="", fg=self.t["accent"], bg=self.t["bg"], font=("Courier New", 18, "bold"))
        self.digital_lbl.pack(side="bottom", pady=(0, 80))
        self.date_lbl = tk.Label(self.right_stack, text="", fg=self.t["lit"], bg=self.t["bg"], font=("Courier New", 16, "bold"))
        self.date_lbl.pack(side="bottom", pady=(0, 15))
        self.icon_bar.place(relx=0.99, rely=0.01, anchor="ne")
        self.toolbar.pack_propagate(False)
        self.iconbitmap("icon.ico")

        if self.is_mini:
            self.right_stack.pack_forget()
            self.main_container.pack_configure(padx=0)
        else:
            self.greeting.pack(side="top", pady=(45, 5), before=self.main_container)

        self.setup_icons()
        self.setup_toolbar() 
        self.draw_grid()
        self.draw_analog_face()

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Map>", self.on_restore)
        self.tick()

    def load_config(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except: pass
        return {"theme": "Tiêu chuẩn", "is_mini": False, "x": 200, "y": 200, "offset_seconds": 0}

    def save_config(self):
        data = {
            "theme": self.theme_name,
            "is_mini": self.is_mini,
            "x": self.winfo_x(),
            "y": self.winfo_y(),
            "offset_seconds": self.offset_seconds
        }
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def on_click(self, event): self.dx, self.dy = event.x, event.y
    def on_drag(self, event): 
        self.geometry(f"+{self.winfo_x()+(event.x-self.dx)}+{self.winfo_y()+(event.y-self.dy)}")
        self.save_config()

    def minimize_window(self):
        self.unbind("<Map>"); self.overrideredirect(False)
        self.iconify()
        self.after(200, lambda: self.bind("<Map>", self.on_restore))

    def on_restore(self, event):
        if self.state() == "normal": self.overrideredirect(True)

    def bind_hover(self, btn, normal_bg, hover_bg, normal_fg, hover_fg):
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg, fg=hover_fg))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg, fg=normal_fg))

    def setup_icons(self):
        for w in self.icon_bar.winfo_children(): w.destroy()
        opt = {"bg": self.t["bg"], "fg": self.t["lit"], "bd": 0, "activebackground": self.t["accent"], "activeforeground": self.t["bg"], "width": 3}
        b1 = tk.Button(self.icon_bar, text="—", font=("Arial", 11, "bold"), command=self.minimize_window, **opt)
        b1.pack(side="left", padx=1)
        self.bind_hover(b1, self.t["bg"], self.t["ui_dim"], self.t["lit"], self.t["accent"])
        b2 = tk.Button(self.icon_bar, text="⚙", font=("Arial", 11), command=self.toggle_toolbar, **opt)
        b2.pack(side="left", padx=1)
        self.bind_hover(b2, self.t["bg"], self.t["ui_dim"], self.t["lit"], self.t["accent"])

    def setup_toolbar(self):
        for w in self.toolbar.winfo_children(): w.destroy()
        btn_opt = {"bg": self.t["bg"], "fg": self.t["lit"], "bd": 0, "padx": 2, "pady": 2, "activebackground": self.t["accent"], "activeforeground": self.t["bg"]}
        
        self.theme_btn = tk.Button(self.toolbar, text="Giao diện", command=self.cycle_theme, **btn_opt)
        self.theme_btn.pack(side="left", expand=True, fill="both")
        
        self.mini_btn = tk.Button(self.toolbar, text="Mini: " + ("Bật" if self.is_mini else "Tắt"), command=self.toggle_mini, **btn_opt)
        self.mini_btn.pack(side="left", expand=True, fill="both")
        
        self.time_grp = tk.Frame(self.toolbar, bg=self.t["bg"])
        self.time_grp.pack(side="left", expand=True, fill="both")
        self.gio_lbl = tk.Label(self.time_grp, text="Giờ:", bg=self.t["bg"], fg=self.t["lit"])
        self.gio_lbl.pack(side="left", padx=(10, 2))
        
        self.h_sp = ttk.Spinbox(self.time_grp, from_=0, to=23, width=3); self.h_sp.pack(side="left")
        self.m_sp = ttk.Spinbox(self.time_grp, from_=0, to=59, width=3); self.m_sp.pack(side="left", padx=2)
        self.s_sp = ttk.Spinbox(self.time_grp, from_=0, to=59, width=3); self.s_sp.pack(side="left")
        
        self.set_btn = tk.Button(self.toolbar, text="Đặt giờ", command=self.set_manual, **btn_opt)
        self.set_btn.pack(side="left", expand=True, fill="both")

        self.reset_btn = tk.Button(self.toolbar, text="Reset giờ", command=self.reset_live, **btn_opt)
        self.reset_btn.pack(side="left", expand=True, fill="both")
        
        self.test_btn = tk.Button(self.toolbar, text="Chạy thử", command=self.toggle_test, **btn_opt)
        self.test_btn.pack(side="left", expand=True, fill="both")
        
        self.close_btn = tk.Button(self.toolbar, text="✕", command=self.destroy, bg="#822", fg="white", bd=0, padx=10, activebackground="#f44")
        self.close_btn.pack(side="left", expand=True, fill="both")
        self.apply_visuals(self.t)

    def cycle_theme(self):
        keys = list(THEMES.keys())
        old_t = self.t.copy()
        self.theme_name = keys[(keys.index(self.theme_name) + 1) % len(keys)]
        new_theme = THEMES[self.theme_name].copy()
        self.save_config()
        self.show_theme_toast(self.theme_name, new_theme)
        self.animate_theme_transition(old_t, new_theme)
        self.t = new_theme

    def animate_theme_transition(self, old_t, new_t, step=0):
        if step > 5: 
            self.draw_analog_face()
            return 
        progress = step / 5
        temp = {k: self.interp_color(old_t[k], new_t[k], progress) for k in ["bg", "grid_dim", "ui_dim", "lit", "accent", "sec"]}
        self.apply_visuals(temp)
        self.after(15, lambda: self.animate_theme_transition(old_t, new_t, step+1))

    def apply_visuals(self, theme):
        self.configure(bg=theme["bg"])
        for w in [self.greeting, self.content_frame, self.main_container, self.word_canvas, self.right_stack, self.analog, self.date_lbl, self.digital_lbl, self.icon_bar, self.toast_lbl, self.time_grp]:
            w.config(bg=theme["bg"])
        self.greeting.config(fg=theme["accent"])
        self.digital_lbl.config(fg=theme["accent"])
        self.date_lbl.config(fg=theme["lit"])
        self.toolbar.config(bg=theme["ui_dim"])
        self.word_canvas.itemconfig("grid_dim", fill=theme["grid_dim"])
        self.word_canvas.itemconfig("grid_lit", fill=theme["lit"])
        self.gio_lbl.config(bg=theme["bg"], fg=theme["lit"])
        for btn in [self.theme_btn, self.set_btn, self.reset_btn]:
            btn.config(bg=theme["bg"], fg=theme["lit"], activebackground=theme["accent"])
            self.bind_hover(btn, theme["bg"], theme["ui_dim"], theme["lit"], theme["accent"])
        for btn in self.icon_bar.winfo_children():
            btn.config(bg=theme["bg"], fg=theme["lit"], activebackground=theme["accent"])
            self.bind_hover(btn, theme["bg"], theme["ui_dim"], theme["lit"], theme["accent"])
        m_bg, m_fg = (theme["accent"], theme["bg"]) if self.is_mini else (theme["bg"], theme["lit"])
        self.mini_btn.config(bg=m_bg, fg=m_fg, activebackground=theme["accent"])
        m_h_bg = theme["lit"] if self.is_mini else theme["ui_dim"]
        self.bind_hover(self.mini_btn, m_bg, m_h_bg, m_fg, theme["accent"] if not self.is_mini else theme["bg"])
        t_bg, t_fg = (theme["accent"], theme["bg"]) if self.test_mode else (theme["bg"], theme["lit"])
        self.test_btn.config(bg=t_bg, fg=t_fg, activebackground=theme["accent"])
        t_h_bg = theme["lit"] if self.test_mode else theme["ui_dim"]
        self.bind_hover(self.test_btn, t_bg, t_h_bg, t_fg, theme["accent"] if not self.test_mode else theme["bg"])

    def show_theme_toast(self, name, new_t):
        if self.is_mini: return
        if self.toast_after_id: self.after_cancel(self.toast_after_id)
        self.toast_lbl.config(text=name.upper(), bg=new_t["bg"], fg=new_t["lit"])
        self.toast_lbl.place(x=20, y=15)
        self.toast_after_id = self.after(500, lambda: self.fade_toast(0, new_t))

    def fade_toast(self, step, theme_at_start):
        if step > 10: 
            self.toast_lbl.config(text="") 
            self.toast_after_id = None
            return
        color = self.interp_color(theme_at_start["lit"], theme_at_start["bg"], step/10)
        self.toast_lbl.config(fg=color)
        self.toast_after_id = self.after(30, lambda: self.fade_toast(step+1, theme_at_start))

    def hex_to_rgb(self, hex_val): return tuple(int(hex_val.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    def rgb_to_hex(self, rgb): return "#%02x%02x%02x" % rgb
    def interp_color(self, c1, c2, t):
        r1, g1, b1 = self.hex_to_rgb(c1); r2, g2, b2 = self.hex_to_rgb(c2)
        return self.rgb_to_hex((int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t)))

    def toggle_toolbar(self):
        self.show_settings = not self.show_settings
        adj = self.TOOLBAR_H if self.show_settings else -self.TOOLBAR_H
        self.geometry(f"{self.winfo_width()}x{self.winfo_height() + adj}")
        if self.show_settings: self.toolbar.pack(side="bottom", fill="x")
        else: self.toolbar.pack_forget()

    def toggle_mini(self):
        self.is_mini = not self.is_mini
        self.show_settings = False
        self.toolbar.pack_forget()
        if self.is_mini:
            self.right_stack.pack_forget()
            self.greeting.pack_forget()
            self.main_container.pack_configure(padx=0) 
            self.geometry(f"{self.MINI_W}x{self.MINI_H}")
        else:
            self.greeting.pack(side="top", pady=(45, 5), before=self.main_container)
            self.right_stack.pack(side="left", fill="y", padx=(50, 0))
            self.main_container.pack_configure(padx=40)
            self.geometry(f"{self.NORM_W}x{self.NORM_H}")
        self.draw_grid()
        self.setup_toolbar() 
        self.active_chars_prev.clear()
        self.save_config()

    def draw_grid(self):
        self.word_canvas.delete("all")
        size, cw, ch = (18, 40, 45) if self.is_mini else (26, 54, 60)
        off_x = (self.MINI_W - (10 * cw)) // 2 if self.is_mini else 0
        off_y = 50 if self.is_mini else 0
        for r in range(6):
            for c in range(10):
                char = GRID_CHARS[r][c].upper()
                x, y = off_x + (c * cw) + (cw // 2), off_y + (r * ch) + (ch // 2)
                self.word_canvas.create_text(x, y, text=char, fill=self.t["grid_dim"], font=("Courier New", size, "bold"), tags="grid_dim")
                lid = self.word_canvas.create_text(x, y, text=char, fill=self.t["lit"], font=("Courier New", size, "bold"), state='hidden', tags="grid_lit")
                self.text_ids[(r,c)] = lid

    def fade_transition(self, tag_id, start_color, end_color, step=0):
        if step > 5: return
        self.word_canvas.itemconfig(tag_id, fill=self.interp_color(start_color, end_color, step/5))
        self.after(30, lambda: self.fade_transition(tag_id, start_color, end_color, step+1))

    def tick(self):
        now = datetime.datetime.now() + datetime.timedelta(seconds=self.offset_seconds)
        
        if self.test_mode:
            self.test_val = (self.test_val + 5) % 1440
            now = datetime.datetime.combine(datetime.date.today(), datetime.time(0)) + datetime.timedelta(minutes=self.test_val)

        h, m, s = now.hour, now.minute, now.second
        self.greeting.config(text="CHÀO BUỔI SÁNG." if 5<=h<12 else "CHÀO BUỔI CHIỀU." if 12<=h<18 else "CHÀO BUỔI TỐI.")
        
        m_round = 5 * round(m/5)
        if m_round == 60: m_round = 0; h += 1
        dh = h % 12 or 12
        active_keys = ["PREFIX", f"HOURS_{dh}", "GIO"] + MINUTE_PATTERNS[m_round] if m_round <= 30 else \
                      ["PREFIX", f"HOURS_{(dh%12)+1}", "GIO", "KEM"] + MINUTE_PATTERNS[60-m_round]

        active_coords = {}
        for k in active_keys:
            if k in WORDS:
                ovr = OVERRIDES.get(k, {})
                for r, c in WORDS[k]: active_coords[(r,c)] = ovr.get((r,c), GRID_CHARS[r][c]).upper()

        curr_set = set(active_coords.keys())
        prev_set = set(self.active_chars_prev.keys())

        for rc in curr_set:
            lid = self.text_ids.get(rc)
            char = active_coords[rc]
            if rc not in prev_set:
                self.word_canvas.itemconfig(lid, text=char, state='normal')
                self.fade_transition(lid, self.t["grid_dim"], self.t["lit"])
            elif self.active_chars_prev[rc] != char:
                self.word_canvas.itemconfig(lid, text=char, state='normal', fill=self.t["lit"])

        for rc in prev_set - curr_set:
            lid = self.text_ids.get(rc)
            self.fade_transition(lid, self.t["lit"], self.t["grid_dim"])
            self.after(200, lambda l=lid: self.word_canvas.itemconfig(l, state='hidden'))
        
        self.active_chars_prev = active_coords
        
        if not self.is_mini:
            self.analog.delete("h"); cx, cy, r = 120, 120, 110
            for a, l, c, w in [(s*6, r-10, self.t["sec"], 1), ((m+s/60)*6, r-30, self.t["accent"], 3), (((h%12)+m/60)*30, r-50, self.t["accent"], 4)]:
                rad = math.radians(a-90); self.analog.create_line(cx, cy, cx+l*math.cos(rad), cy+l*math.sin(rad), fill=c, width=w, tags="h", capstyle="round")
            self.digital_lbl.config(text=now.strftime('%H:%M:%S'))
            self.date_lbl.config(text=f"{DAYS_VN[now.weekday()]}, {now.strftime('%d/%m/%Y')}")

        self.after(500 if self.test_mode else 1000, self.tick)

    def draw_analog_face(self):
        self.analog.delete("face"); cx, cy, r = 120, 120, 110
        face_color = self.t["ui_dim"]
        self.analog.create_oval(cx-r, cy-r, cx+r, cy+r, outline=face_color, width=2, tags="face")
        for i in range(12):
            a = math.radians(i*30-90)
            color = self.t["ui_dim"]
            self.analog.create_line(cx+(r-2)*math.cos(a), cy+(r-2)*math.sin(a), cx+(r-12)*math.cos(a), cy+(r-12)*math.sin(a), fill=color, width=2, tags="face")

    def set_manual(self): 
        try:
            h = int(self.h_sp.get() or 0)
            m = int(self.m_sp.get() or 0)
            s = int(self.s_sp.get() or 0)
            
            now = datetime.datetime.now()
            target = now.replace(hour=h, minute=m, second=s, microsecond=0)
            
            self.offset_seconds = (target - now).total_seconds()
            
            self.test_mode = False
            self.save_config()
            self.apply_visuals(self.t)
        except ValueError:
            pass

    def reset_live(self): 
        self.offset_seconds = 0
        self.test_mode = False
        self.save_config()
        self.apply_visuals(self.t)

    def toggle_test(self): 
        self.test_mode = not self.test_mode
        self.apply_visuals(self.t)

if __name__ == "__main__":
    StudioClock().mainloop()