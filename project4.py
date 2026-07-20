import tkinter as tk
from tkinter import messagebox
import math

# --- Class 1: TransferFunction (Negahdari moshakhasat system) ---
class TransferFunction:
    def __init__(self, bahre_k=1.0, zarib_mirai=0.5, fr_tabiei=1.0):
        self.bahre_k = bahre_k
        self.zarib_mirai = zarib_mirai
        self.fr_tabiei = fr_tabiei

# --- Class 2: StepResponse (Mohasebe dade-haye nemodar) ---
class StepResponse:
    def __init__(self, tf):
        self.tf = tf
        self.list_zaman = []
        self.list_khoroji = []

    def mohasebe_noghat(self, modat_zaman=20, gam=0.1):
        self.list_zaman = []
        self.list_khoroji = []
        
        k = self.tf.bahre_k
        z = self.tf.zarib_mirai
        wn = self.tf.fr_tabiei
        
        t = 0
        while t <= modat_zaman:
            # Formool pasokh pele system martabe dovom
            if z < 1:  # Underdamped (Namosani)
                wd = wn * math.sqrt(1 - z**2)
                phi = math.acos(z)
                y = k * (1 - (1/math.sqrt(1 - z**2)) * math.exp(-z * wn * t) * math.sin(wd * t + phi))
            elif z == 1: # Critically damped
                y = k * (1 - math.exp(-wn * t) * (1 + wn * t))
            else: # Overdamped (Kond)
                r1 = -wn * (z - math.sqrt(z**2 - 1))
                r2 = -wn * (z + math.sqrt(z**2 - 1))
                c1 = k * r2 / (r2 - r1)
                c2 = k * r1 / (r1 - r2)
                y = k + c1 * math.exp(r1 * t) + c2 * math.exp(r2 * t)
            
            self.list_zaman.append(t)
            self.list_khoroji.append(y)
            t += gam
        return self.list_zaman, self.list_khoroji

# --- Class 3: Analyzer (Estekhraj moshakhasat pasokh) ---
class Analyzer:
    def __init__(self, list_zaman, list_khoroji, bahre_k):
        self.list_zaman = list_zaman
        self.list_khoroji = list_khoroji
        self.bahre_k = bahre_k

    def tahlil_system(self):
        if not self.list_khoroji:
            return None

        # 1. Max Khoroji & Overshoot
        max_y = max(self.list_khoroji)
        overshoot_meghdar = ((max_y - self.bahre_k) / self.bahre_k) * 100
        if overshoot_meghdar < 0: overshoot_meghdar = 0

        # 2. Zaman Sood (Rise Time: 10% ta 90% meghdar-e nahaee)
        t10 = t90 = 0
        for i, y in enumerate(self.list_khoroji):
            if y >= 0.1 * self.bahre_k and t10 == 0:
                t10 = self.list_zaman[i]
            if y >= 0.9 * self.bahre_k and t90 == 0:
                t90 = self.list_zaman[i]
        zaman_sood = t90 - t10

        # 3. Zaman Neshast (Settling Time: ba khataye 2%)
        zaman_neshast = 0
        for i in range(len(self.list_khoroji) - 1, -1, -1):
            if abs(self.list_khoroji[i] - self.bahre_k) > 0.02 * self.bahre_k:
                zaman_neshast = self.list_zaman[i]
                break

        return {
            "overshoot": overshoot_meghdar,
            "zaman_sood": zaman_sood,
            "zaman_neshast": zaman_neshast
        }

# --- Class 4: Plotter (Rasm-e nemodar dar GUI) ---
class Plotter:
    def __init__(self, canvas):
        self.canvas = canvas

    def rasm_khat(self, list_zaman, list_khoroji, bahre_k):
        self.canvas.delete("all")
        w, h = 550, 350
        padding = 40
        
        # Rasm-e mehvar-ha
        self.canvas.create_line(padding, h-padding, w-padding, h-padding, width=2) # X
        self.canvas.create_line(padding, padding, padding, h-padding, width=2) # Y
        
        if not list_khoroji: return

        max_t = max(list_zaman)
        max_y = max(max(list_khoroji), bahre_k) * 1.2 # Baraye inke namosad az kadr biron nazane
        
        # Tabdil mokhtassat be pixel
        def to_px(t, y):
            px = padding + (t / max_t) * (w - 2 * padding)
            py = (h - padding) - (y / max_y) * (h - 2 * padding)
            return px, py

        # Rasm-e khat-e Setpoint (Hadaf)
        hx1, hy1 = to_px(0, bahre_k)
        hx2, hy2 = to_px(max_t, bahre_k)
        self.canvas.create_line(hx1, hy1, hx2, hy2, fill="red", dash=(4,2))

        # Rasm-e monhani pasokh
        for i in range(len(list_zaman) - 1):
            x1, y1 = to_px(list_zaman[i], list_khoroji[i])
            x2, y2 = to_px(list_zaman[i+1], list_khoroji[i+1])
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)

# --- Class 5: GUI (Main App) ---
class ControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tahlil-gar System-haye Controli")
        self.root.geometry("600x650")

        # Bakhsh-e vorodi-ha
        frame_input = tk.Frame(root)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Gain (K):").grid(row=0, column=0)
        self.ent_k = tk.Entry(frame_input, width=10)
        self.ent_k.insert(0, "1.0")
        self.ent_k.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="Zeta (ζ):").grid(row=0, column=2)
        self.ent_zeta = tk.Entry(frame_input, width=10)
        self.ent_zeta.insert(0, "0.5")
        self.ent_zeta.grid(row=0, column=3, padx=5)

        tk.Label(frame_input, text="Wn (ωn):").grid(row=1, column=0, pady=5)
        self.ent_wn = tk.Entry(frame_input, width=10)
        self.ent_wn.insert(0, "2.0")
        self.ent_wn.grid(row=1, column=1, padx=5)

        btn_tahlil = tk.Button(frame_input, text="Mohasebe & Rasm", command=self.ejra, bg="lightgreen")
        btn_tahlil.grid(row=1, column=2, columnspan=2, sticky="we", padx=5)

        # Bakhsh-e Nemodar
        self.canvas = tk.Canvas(root, width=550, height=350, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=10)
        self.plotter = Plotter(self.canvas)

        # Bakhsh-e Natije
        self.lbl_res = tk.Label(root, text="Natije tahlil dar inja namayesh dade mishavad.", font=("Arial", 10, "bold"), fg="darkblue")
        self.lbl_res.pack(pady=10)

    def ejra(self):
        try:
            k = float(self.ent_k.get())
            z = float(self.ent_zeta.get())
            wn = float(self.ent_wn.get())
            
            # 1. Sakht-e System
            tf = TransferFunction(k, z, wn)
            
            # 2. Mohasebe Pasokh
            resp = StepResponse(tf)
            tz, yz = resp.mohasebe_noghat()
            
            # 3. Tahlil
            analyzer = Analyzer(tz, yz, k)
            natayej = analyzer.tahlil_system()
            
            # 4. Namayesh
            self.plotter.rasm_khat(tz, yz, k)
            
            matn = (f"Overshoot: {natayej['overshoot']:.2f}%\n"
                    f"Zaman Sood: {natayej['zaman_sood']:.2f} s\n"
                    f"Zaman Neshast: {natayej['zaman_neshast']:.2f} s")
            self.lbl_res.config(text=matn)
            
        except Exception as e:
            messagebox.showerror("Error", "Lotfan adad-haye dorost vared konid!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ControlApp(root)
    root.mainloop()
