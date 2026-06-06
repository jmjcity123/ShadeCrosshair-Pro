import sys
import subprocess
import tkinter as tk
from tkinter import ttk, colorchooser
import json
import os

# Installation der benötigten Windows-Bibliotheken
try:
    import win32gui, win32con
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
    import win32gui, win32con

CONFIG_FILE = "settings.json"

class CrosshairStudio:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Einstellungen laden
        self.settings = self.load_settings()
        
        # Overlay Fenster
        self.ov = tk.Toplevel(self.root)
        self.ov.overrideredirect(True)
        self.ov.attributes("-topmost", True)
        self.ov.attributes("-transparentcolor", "black")
        self.ov.config(bg="black")
        
        self.size = self.settings["size"]
        self.color = self.settings["color"]
        self.shape = self.settings["shape"]
        
        self.canvas = tk.Canvas(self.ov, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        hwnd = win32gui.GetParent(self.ov.winfo_id())
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        
        self.show_menu()
        self.menu.protocol("WM_DELETE_WINDOW", self.exit_app)
        
        self.draw()
        self.root.mainloop()

    def load_settings(self):
        """Lädt Einstellungen aus der JSON-Datei."""
        default = {"size": 200, "color": "#00FF00", "shape": "Kreuz"}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return {**default, **json.load(f)}
            except:
                return default
        return default

    def save_settings(self):
        """Speichert den aktuellen Zustand in der JSON-Datei."""
        data = {"size": self.size, "color": self.color, "shape": self.shape}
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)

    def show_menu(self):
        self.menu = tk.Toplevel(self.root)
        self.menu.title("HUD Settings")
        self.menu.geometry("320x450")
        self.menu.configure(bg="#121212")
        
        ttk.Label(self.menu, text="CROSSHAIR HUD", background="#121212", foreground="#00FF00", font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        btn_frame = tk.Frame(self.menu, bg="#121212")
        btn_frame.pack(side="bottom", pady=30, fill="x", padx=20)
        
        for s in ["Kreuz", "Kreis", "Quadrat", "Punkt"]:
            tk.Button(btn_frame, text=s, command=lambda x=s: self.change_shape(x), 
                      bg="#1f1f1f", fg="white", activebackground="#333", relief="flat", height=2).pack(fill="x", pady=2)
        
        ttk.Label(self.menu, text="SKALIERUNG", background="#121212", foreground="#888").pack(pady=(10, 0))
        s = ttk.Scale(self.menu, from_=50, to=400, orient="horizontal", command=self.change_size)
        s.set(self.size)
        s.pack(fill="x", padx=30, pady=10)
        
        tk.Button(self.menu, text="Farbe wählen", command=self.pick_color, bg="#1f1f1f", fg="white", relief="flat").pack(pady=10)

    def exit_app(self):
        self.ov.destroy()
        self.root.destroy()

    def change_shape(self, shape): 
        self.shape = shape; self.draw(); self.save_settings()
        
    def change_size(self, v): 
        self.size = int(float(v)); self.draw(); self.save_settings()
        
    def pick_color(self): 
        c = colorchooser.askcolor()[1]
        if c: self.color = c; self.draw(); self.save_settings()

    def draw(self):
        self.canvas.delete("all")
        self.ov.geometry(f"{self.size}x{self.size}+{self.root.winfo_screenwidth()//2-self.size//2}+{self.root.winfo_screenheight()//2-self.size//2}")
        c = self.size // 2
        L = self.size * 0.075
        G = self.size * 0.0375
        W = max(1, self.size * 0.02)
        
        if self.shape == "Kreuz":
            self.canvas.create_line(c-G-L, c, c-G, c, fill=self.color, width=W)
            self.canvas.create_line(c+G, c, c+G+L, c, fill=self.color, width=W)
            self.canvas.create_line(c, c-G-L, c, c-G, fill=self.color, width=W)
            self.canvas.create_line(c, c+G, c, c+G+L, fill=self.color, width=W)
        elif self.shape == "Kreis": self.canvas.create_oval(c-L, c-L, c+L, c+L, outline=self.color, width=W)
        elif self.shape == "Quadrat": self.canvas.create_rectangle(c-L, c-L, c+L, c+L, outline=self.color, width=W)
        elif self.shape == "Punkt": self.canvas.create_oval(c-W*2, c-W*2, c+W*2, c+W*2, fill=self.color, outline=self.color)

if __name__ == "__main__":
    CrosshairStudio()