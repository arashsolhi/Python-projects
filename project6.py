import tkinter as tk
from tkinter import messagebox


class Passenger:
    def __init__(self, esm, noe_harekat):
        self.esm = esm
        self.noe_harekat = noe_harekat
        self.rad_shode = False


class Card:
    def __init__(self, motabar=True, mojodi=5):
        self.motabar = motabar
        self.mojodi = mojodi

    def check_card(self):
        return self.motabar and self.mojodi > 0

    def use_card(self):
        if self.check_card():
            self.mojodi -= 1
            return True
        return False


class Sensor:
    def __init__(self, noe_sensor):
        self.noe_sensor = noe_sensor
        self.faol = False

    def tashkhis_kart(self, card):
        self.faol = True
        return card.check_card()

    def tashkhis_mosafer(self, passenger):
        self.faol = True
        return passenger is not None

    def reset(self):
        self.faol = False


class Motor:
    def __init__(self):
        self.vaziat = "baste"

    def baz_kardan(self):
        self.vaziat = "baz"

    def baste_kardan(self):
        self.vaziat = "baste"


class Gate:
    def __init__(self):
        self.card_sensor = Sensor("card")
        self.passenger_sensor = Sensor("passenger")
        self.motor = Motor()
        self.vaziat = "entezar"
        self.passenger = None
        self.card = None
        self.log = ""

    def add_passenger(self, passenger):
        self.passenger = passenger
        self.vaziat = "mosafer_amade"
        self.log = f"{passenger.esm} baraye {passenger.noe_harekat} amad."

    def set_card(self, card):
        self.card = card

    def process(self):
        if self.passenger is None:
            self.log = "Mosafer mojood nist."
            return False

        if self.card is None:
            self.log = "Kart mojood nist."
            return False

        card_ok = self.card_sensor.tashkhis_kart(self.card)
        passenger_ok = self.passenger_sensor.tashkhis_mosafer(self.passenger)

        if card_ok and passenger_ok and self.card.use_card():
            self.motor.baz_kardan()
            self.vaziat = "gate_baz"
            self.log = "Kart motabar ast. Gate baz shod."
            return True

        self.vaziat = "error"
        self.log = "Kart namotabar ast ya mojodi kafi nist."
        return False

    def oboor_mosafer(self):
        if self.passenger is not None and self.motor.vaziat == "baz":
            self.passenger.rad_shode = True
            self.vaziat = "oboor"
            self.log = f"{self.passenger.esm} az gate rad shod."
            return True
        return False

    def close_gate(self):
        self.motor.baste_kardan()
        self.vaziat = "baste"
        self.card_sensor.reset()
        self.passenger_sensor.reset()
        self.card = None
        self.passenger = None
        self.log = "Gate baste shod."

    def update_vaziat(self):
        return self.motor.vaziat, self.vaziat, self.log


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Metro Gate Simulator")
        self.root.geometry("850x600")

        self.gate = Gate()
        self.shomare_mosafer = 1

        tk.Label(root, text="Metro Gate Simulator", font=("Arial", 18, "bold")).pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Button(frame, text="Mosafer Vorood", width=16, command=self.add_vorood).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame, text="Kart Motabar", width=16, command=self.set_valid_card).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Kart Namotabar", width=16, command=self.set_invalid_card).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(frame, text="Check Gate", width=16, command=self.process_gate).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame, text="Oboor Mosafer", width=16, command=self.pass_passenger).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame, text="Reset", width=16, command=self.reset_gate).grid(row=1, column=2, padx=5, pady=5)

        self.canvas = tk.Canvas(root, width=700, height=260, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=20)

        self.lbl_status = tk.Label(root, text="Gate: baste | System: entezar", font=("Arial", 12))
        self.lbl_status.pack(pady=5)

        self.lbl_log = tk.Label(root, text="Amadeh baraye shabih sazi", font=("Arial", 11), fg="darkblue")
        self.lbl_log.pack(pady=5)

        self.draw_gate()

    def add_vorood(self):
        passenger = Passenger(f"Mosafer {self.shomare_mosafer}", "vorood")
        self.shomare_mosafer += 1
        self.gate.add_passenger(passenger)
        self.refresh()

    def set_valid_card(self):
        self.gate.set_card(Card(True, 5))
        self.gate.log = "Kart motabar sabt shod."
        self.refresh()

    def set_invalid_card(self):
        self.gate.set_card(Card(False, 0))
        self.gate.log = "Kart namotabar sabt shod."
        self.refresh()

    def process_gate(self):
        ok = self.gate.process()
        self.refresh()
        if not ok:
            messagebox.showerror("Error", self.gate.log)

    def pass_passenger(self):
        ok = self.gate.oboor_mosafer()
        self.refresh()
        if ok:
            self.root.after(1000, self.auto_close_gate)

    def auto_close_gate(self):
        self.gate.close_gate()
        self.refresh()

    def reset_gate(self):
        self.gate = Gate()
        self.refresh()

    def refresh(self):
        gate_vaziat, system_vaziat, log = self.gate.update_vaziat()
        self.lbl_status.config(text=f"Gate: {gate_vaziat} | System: {system_vaziat}")
        self.lbl_log.config(text=log)
        self.draw_gate()

    def draw_gate(self):
        self.canvas.delete("all")

        self.canvas.create_rectangle(200, 80, 500, 200, outline="black", width=2, fill="#e8e8e8")
        self.canvas.create_rectangle(320, 80, 380, 200, fill="white", outline="gray")

        if self.gate.motor.vaziat == "baste":
            self.canvas.create_rectangle(300, 90, 320, 190, fill="red")
            self.canvas.create_rectangle(380, 90, 400, 190, fill="red")
            gate_text = "Gate Baste Ast"
            color_text = "red"
        else:
            self.canvas.create_rectangle(260, 90, 280, 190, fill="green")
            self.canvas.create_rectangle(420, 90, 440, 190, fill="green")
            gate_text = "Gate Baz Ast"
            color_text = "green"

        self.canvas.create_rectangle(220, 110, 270, 140, fill="lightblue", outline="black")
        self.canvas.create_text(245, 125, text="Card Sensor", font=("Arial", 9))

        self.canvas.create_rectangle(430, 110, 480, 140, fill="lightyellow", outline="black")
        self.canvas.create_text(455, 125, text="Passenger Sensor", font=("Arial", 8))

        if self.gate.passenger is not None:
            x = 120
            y = 140
            if self.gate.passenger.rad_shode:
                x = 600

            self.canvas.create_oval(x, y - 30, x + 30, y, fill="peachpuff", outline="black")
            self.canvas.create_line(x + 15, y, x + 15, y + 45, width=3)
            self.canvas.create_line(x + 15, y + 15, x - 5, y + 30, width=2)
            self.canvas.create_line(x + 15, y + 15, x + 35, y + 30, width=2)
            self.canvas.create_line(x + 15, y + 45, x, y + 70, width=2)
            self.canvas.create_line(x + 15, y + 45, x + 30, y + 70, width=2)
            self.canvas.create_text(x + 15, y + 85, text=self.gate.passenger.noe_harekat, font=("Arial", 10))

        self.canvas.create_text(350, 40, text=gate_text, font=("Arial", 16, "bold"), fill=color_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
