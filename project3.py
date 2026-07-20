import tkinter as tk
from tkinter import ttk
import random
import math


class Tank:
    def __init__(self, masahat_tank=1.0, level_avaliye=20.0, max_level=100.0, zarb_khoroji=0.15):
        self.masahat_tank = masahat_tank
        self.level_ab = level_avaliye
        self.level_avaliye = level_avaliye
        self.max_level = max_level
        self.zarb_khoroji = zarb_khoroji

    def update_level(self, debi_vorodi, gam_zamani):
        debi_khoroji = self.zarb_khoroji * math.sqrt(max(self.level_ab, 0))
        taghir_level = (debi_vorodi - debi_khoroji) / self.masahat_tank
        self.level_ab += taghir_level * gam_zamani

        if self.level_ab < 0:
            self.level_ab = 0
        if self.level_ab > self.max_level:
            self.level_ab = self.max_level

        return debi_khoroji


class Pump:
    def __init__(self, max_debi=10.0):
        self.max_debi = max_debi
        self.debi = 0.0

    def set_debi(self, meghdar):
        if meghdar < 0:
            meghdar = 0
        if meghdar > self.max_debi:
            meghdar = self.max_debi
        self.debi = meghdar

    def get_debi(self):
        return self.debi


class Sensor:
    def __init__(self, meghdar_noise=0.5):
        self.meghdar_noise = meghdar_noise

    def khondan_level(self, level_vagheii):
        noise_tasadofi = random.uniform(-self.meghdar_noise, self.meghdar_noise)
        level_andaze_giri = level_vagheii + noise_tasadofi
        if level_andaze_giri < 0:
            level_andaze_giri = 0
        return level_andaze_giri


class Controller:
    def __init__(self, noe_control="ON_OFF", level_matloob=50.0):
        self.noe_control = noe_control
        self.level_matloob = level_matloob

        self.kp = 0.8
        self.ki = 0.03
        self.kd = 0.2

        self.majmooe_khata = 0.0
        self.khata_ghabli = 0.0

    def set_noe_control(self, noe_jadid):
        self.noe_control = noe_jadid
        self.majmooe_khata = 0.0
        self.khata_ghabli = 0.0

    def set_level_matloob(self, level_jadid):
        self.level_matloob = level_jadid

    def mohasebe_control(self, level_andaze_giri, gam_zamani, max_debi):
        khata = self.level_matloob - level_andaze_giri

        if self.noe_control == "ON_OFF":
            if khata > 1:
                khoroji_control = max_debi
            elif khata < -1:
                khoroji_control = 0
            else:
                khoroji_control = max_debi / 2
            return khoroji_control

        elif self.noe_control == "PID":
            self.majmooe_khata += khata * gam_zamani
            moshtagh_khata = (khata - self.khata_ghabli) / gam_zamani

            khoroji_control = (
                self.kp * khata
                + self.ki * self.majmooe_khata
                + self.kd * moshtagh_khata
            )

            self.khata_ghabli = khata

            if khoroji_control < 0:
                khoroji_control = 0
            if khoroji_control > max_debi:
                khoroji_control = max_debi

            return khoroji_control

        return 0.0


class Simulation:
    def __init__(self):
        self.tank = Tank()
        self.pump = Pump()
        self.sensor = Sensor()
        self.controller = Controller()

        self.zaman = 0.0
        self.gam_zamani = 0.5

        self.list_zaman = []
        self.list_level = []
        self.list_debi = []
        self.list_level_matloob = []

    def reset_kardan(self):
        self.tank = Tank(
            masahat_tank=self.tank.masahat_tank,
            level_avaliye=self.tank.level_avaliye,
            max_level=self.tank.max_level,
            zarb_khoroji=self.tank.zarb_khoroji
        )
        self.pump = Pump(max_debi=self.pump.max_debi)
        self.sensor = Sensor(meghdar_noise=self.sensor.meghdar_noise)

        noe_control_feli = self.controller.noe_control
        level_matloob_feli = self.controller.level_matloob
        self.controller = Controller(noe_control=noe_control_feli, level_matloob=level_matloob_feli)

        self.zaman = 0.0
        self.list_zaman = []
        self.list_level = []
        self.list_debi = []
        self.list_level_matloob = []

    def yek_gam(self):
        level_andaze_giri = self.sensor.khondan_level(self.tank.level_ab)

        debi_vorodi = self.controller.mohasebe_control(
            level_andaze_giri,
            self.gam_zamani,
            self.pump.max_debi
        )

        self.pump.set_debi(debi_vorodi)
        debi_vorodi = self.pump.get_debi()

        debi_khoroji = self.tank.update_level(debi_vorodi, self.gam_zamani)

        self.zaman += self.gam_zamani

        self.list_zaman.append(self.zaman)
        self.list_level.append(self.tank.level_ab)
        self.list_debi.append(debi_vorodi)
        self.list_level_matloob.append(self.controller.level_matloob)

        return {
            "zaman": self.zaman,
            "level_vagheii": self.tank.level_ab,
            "level_andaze_giri": level_andaze_giri,
            "debi_vorodi": debi_vorodi,
            "debi_khoroji": debi_khoroji,
            "level_matloob": self.controller.level_matloob
        }


class TankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shabih Sazi Tank Ab")
        self.root.geometry("950x650")

        self.sim = Simulation()
        self.ejraye_khodkar = False

        self.sakhte_dokmeha()
        self.update_namayesh()

    def sakhte_dokmeha(self):
        frame_bala = tk.Frame(self.root)
        frame_bala.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(frame_bala, text="Noe Control:").grid(row=0, column=0, padx=5, pady=5)
        self.noe_control_var = tk.StringVar(value="ON_OFF")
        combo = ttk.Combobox(
            frame_bala,
            textvariable=self.noe_control_var,
            values=["ON_OFF", "PID"],
            state="readonly",
            width=10
        )
        combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_bala, text="Level Matloob:").grid(row=0, column=2, padx=5, pady=5)
        self.level_matloob_var = tk.StringVar(value="50")
        entry = tk.Entry(frame_bala, textvariable=self.level_matloob_var, width=10)
        entry.grid(row=0, column=3, padx=5, pady=5)

        btn_emal = tk.Button(frame_bala, text="Emal Tanzimat", command=self.emal_tanzimat)
        btn_emal.grid(row=0, column=4, padx=5, pady=5)

        btn_gam = tk.Button(frame_bala, text="Yek Gam", command=self.yek_gam_shabih_sazi)
        btn_gam.grid(row=0, column=5, padx=5, pady=5)

        self.btn_auto = tk.Button(frame_bala, text="Shoroo Auto", command=self.taghir_ejra_khodkar)
        self.btn_auto.grid(row=0, column=6, padx=5, pady=5)

        btn_reset = tk.Button(frame_bala, text="Reset", command=self.reset_shabih_sazi)
        btn_reset.grid(row=0, column=7, padx=5, pady=5)

        self.label_ettelat = tk.Label(self.root, text="", justify="left", font=("Arial", 11))
        self.label_ettelat.pack(pady=10)

        frame_paein = tk.Frame(self.root)
        frame_paein.pack(fill=tk.BOTH, expand=True)

        self.canvas_tank = tk.Canvas(frame_paein, width=300, height=450, bg="white")
        self.canvas_tank.pack(side=tk.LEFT, padx=20, pady=10)

        self.canvas_nemodar = tk.Canvas(frame_paein, width=580, height=450, bg="white")
        self.canvas_nemodar.pack(side=tk.RIGHT, padx=20, pady=10)

    def emal_tanzimat(self):
        noe_jadid = self.noe_control_var.get()
        self.sim.controller.set_noe_control(noe_jadid)

        try:
            level_jadid = float(self.level_matloob_var.get())
        except ValueError:
            level_jadid = 50.0
            self.level_matloob_var.set("50")

        if level_jadid < 0:
            level_jadid = 0
        if level_jadid > self.sim.tank.max_level:
            level_jadid = self.sim.tank.max_level

        self.sim.controller.set_level_matloob(level_jadid)
        self.update_namayesh()

    def yek_gam_shabih_sazi(self):
        self.sim.yek_gam()
        self.update_namayesh()

    def taghir_ejra_khodkar(self):
        self.ejraye_khodkar = not self.ejraye_khodkar

        if self.ejraye_khodkar:
            self.btn_auto.config(text="Stop Auto")
            self.ejra_khodkar()
        else:
            self.btn_auto.config(text="Shoroo Auto")

    def ejra_khodkar(self):
        if self.ejraye_khodkar:
            self.sim.yek_gam()
            self.update_namayesh()
            self.root.after(500, self.ejra_khodkar)

    def reset_shabih_sazi(self):
        self.ejraye_khodkar = False
        self.btn_auto.config(text="Shoroo Auto")
        self.sim.reset_kardan()
        self.update_namayesh()

    def update_ettelat(self):
        khata = self.sim.controller.level_matloob - self.sim.tank.level_ab

        matn = (
            f"Zaman: {self.sim.zaman:.1f} s\n"
            f"Level Ab: {self.sim.tank.level_ab:.2f}\n"
            f"Level Matloob: {self.sim.controller.level_matloob:.2f}\n"
            f"Khata: {khata:.2f}\n"
            f"Debi Pump: {self.sim.pump.get_debi():.2f}\n"
            f"Noe Control: {self.sim.controller.noe_control}"
        )

        self.label_ettelat.config(text=matn)

    def rasm_tank(self):
        self.canvas_tank.delete("all")

        x1 = 80
        y1 = 50
        x2 = 220
        y2 = 400

        self.canvas_tank.create_rectangle(x1, y1, x2, y2, outline="black", width=2)

        ertefae_kol = y2 - y1
        nesbat_ab = self.sim.tank.level_ab / self.sim.tank.max_level
        ertefae_ab = ertefae_kol * nesbat_ab

        self.canvas_tank.create_rectangle(
            x1 + 1,
            y2 - ertefae_ab,
            x2 - 1,
            y2 - 1,
            fill="deepskyblue",
            outline=""
        )

        nesbat_hadaf = self.sim.controller.level_matloob / self.sim.tank.max_level
        y_hadaf = y2 - (ertefae_kol * nesbat_hadaf)

        self.canvas_tank.create_line(x1 - 20, y_hadaf, x2 + 20, y_hadaf, fill="red", dash=(4, 2), width=2)
        self.canvas_tank.create_text(150, 25, text="Tank Ab", font=("Arial", 14, "bold"))
        self.canvas_tank.create_text(150, 420, text=f"Level: {self.sim.tank.level_ab:.2f}", font=("Arial", 12))

    def rasm_nemodar(self):
        self.canvas_nemodar.delete("all")

        x1 = 50
        y1 = 30
        x2 = 550
        y2 = 400

        self.canvas_nemodar.create_rectangle(x1, y1, x2, y2, outline="black")

        self.canvas_nemodar.create_text(300, 15, text="Nemodar Taghirat Level", font=("Arial", 13, "bold"))
        self.canvas_nemodar.create_text(300, 425, text="Zaman", font=("Arial", 11))
        self.canvas_nemodar.create_text(18, 210, text="Level", angle=90, font=("Arial", 11))

        if len(self.sim.list_zaman) < 2:
            return

        max_zaman = max(self.sim.list_zaman)
        if max_zaman == 0:
            max_zaman = 1

        max_level = self.sim.tank.max_level

        noghat_level = []
        noghat_hadaf = []

        for i in range(len(self.sim.list_zaman)):
            zaman = self.sim.list_zaman[i]
            level = self.sim.list_level[i]
            hadaf = self.sim.list_level_matloob[i]

            x = x1 + (zaman / max_zaman) * (x2 - x1)
            y_level = y2 - (level / max_level) * (y2 - y1)
            y_hadaf = y2 - (hadaf / max_level) * (y2 - y1)

            noghat_level.append((x, y_level))
            noghat_hadaf.append((x, y_hadaf))

        for i in range(len(noghat_level) - 1):
            self.canvas_nemodar.create_line(
                noghat_level[i][0], noghat_level[i][1],
                noghat_level[i + 1][0], noghat_level[i + 1][1],
                fill="blue", width=2
            )

            self.canvas_nemodar.create_line(
                noghat_hadaf[i][0], noghat_hadaf[i][1],
                noghat_hadaf[i + 1][0], noghat_hadaf[i + 1][1],
                fill="red", dash=(4, 2), width=2
            )

        self.canvas_nemodar.create_text(460, 40, text="Blue: Level", fill="blue", font=("Arial", 10))
        self.canvas_nemodar.create_text(465, 60, text="Red: Setpoint", fill="red", font=("Arial", 10))

    def update_namayesh(self):
        self.update_ettelat()
        self.rasm_tank()
        self.rasm_nemodar()


if __name__ == "__main__":
    root = tk.Tk()
    app = TankApp(root)
    root.mainloop()
