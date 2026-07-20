import tkinter as tk
from tkinter import messagebox


Time_sabz = 6
Obor_mashin = 2
Name_masir = ["north", "south", "east", "west"]


class Car:
    def __init__(self, shomare_mashin, vorod_besaf):
        self.shomare_mashin = shomare_mashin
        self.vorod_besaf = vorod_besaf

    def entezar(self, current_time):
        return current_time - self.vorod_besaf


class Lane:
    def __init__(self, name):
        self.name = name
        self.saf_mashin = []

    def add_car(self, car):
        self.saf_mashin.append(car)

    def remove_cars(self, count):
        obor_karde = self.saf_mashin[:count]
        self.saf_mashin = self.saf_mashin[count:]
        return obor_karde

    def tedad_mashin(self):
        return len(self.saf_mashin)


class TrafficLight:
    def __init__(self, name):
        self.name = name
        self.color = "red"

    def rang_cheragh(self, color):
        self.color = color


class Intersection:
    def __init__(self):
        self.lanes = {}
        self.lights = {}

        for name in Name_masir:
            self.lanes[name] = Lane(name)
            self.lights[name] = TrafficLight(name)


class Controller:
    def __init__(self, intersection):
        self.intersection = intersection
        self.time = 0
        self.masir_sabz = "ns"
        self.time_sabz = Time_sabz
        self.shomare_mashine_badi = 1
        self.tedad_mashin_radshode = 0
        self.akharin_vazeiat = "System started"
        self.tanzim_cheragh()

    def tanzim_cheragh(self):
        if self.masir_sabz == "ns":
            self.intersection.lights["north"].rang_cheragh("green")
            self.intersection.lights["south"].rang_cheragh("green")
            self.intersection.lights["east"].rang_cheragh("red")
            self.intersection.lights["west"].rang_cheragh("red")
        else:
            self.intersection.lights["north"].rang_cheragh("red")
            self.intersection.lights["south"].rang_cheragh("red")
            self.intersection.lights["east"].rang_cheragh("green")
            self.intersection.lights["west"].rang_cheragh("green")

    def add_car(self, lane_name, count=1):
        if lane_name not in self.intersection.lanes:
            self.akharin_vazeiat = "Invalid lane"
            return False

        for _ in range(count):
            car = Car(self.shomare_mashine_badi, self.time)
            self.intersection.lanes[lane_name].add_car(car)
            self.shomare_mashine_badi += 1

        self.akharin_vazeiat = f"{count} car(s) added to {lane_name}"
        return True

    def gereftan_masir_sabz(self):
        if self.masir_sabz == "ns":
            return ["north", "south"]
        return ["east", "west"]

    def taviz_cheragh(self):
        if self.masir_sabz == "ns":
            self.masir_sabz = "ew"
        else:
            self.masir_sabz = "ns"

        self.time_sabz = Time_sabz
        self.tanzim_cheragh()

    def obor_dadan_mashinha(self):
        passed_now = 0
        green_lanes = self.gereftan_masir_sabz()

        remaining = Obor_mashin

        for lane_name in green_lanes:
            if remaining <= 0:
                break

            lane = self.intersection.lanes[lane_name]
            can_pass = min(remaining, lane.tedad_mashin())
            obor_karde = lane.remove_cars(can_pass)
            passed_now += len(obor_karde)
            remaining -= len(obor_karde)

        self.tedad_mashin_radshode += passed_now
        return passed_now

    def step(self):
        self.time += 1

        passed_now = self.obor_dadan_mashinha()

        self.time_sabz -= 1
        switched = False

        if self.time_sabz <= 0:
            self.taviz_cheragh()
            switched = True

        if switched:
            self.akharin_vazeiat = f"Time={self.time}, passed={passed_now}, lights switched to {self.masir_sabz}"
        else:
            self.akharin_vazeiat = f"Time={self.time}, passed={passed_now}, remaining_green={self.time_sabz}"

    def tedad_mashin_montazer(self):
        total = 0
        for lane in self.intersection.lanes.values():
            total += lane.tedad_mashin()
        return total

    def miangir_entezar(self):
        total_wait = 0
        total_cars = 0

        for lane in self.intersection.lanes.values():
            for car in lane.saf_mashin:
                total_wait += car.entezar(self.time)
                total_cars += 1

        if total_cars == 0:
            return 0.0

        return total_wait / total_cars


class TrafficGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Traffic Light Simulator")

        self.intersection = Intersection()
        self.controller = Controller(self.intersection)
        self.auto_run = False

        self.create_widgets()
        self.update_view()

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Lane").grid(row=0, column=0, padx=5)
        self.lane_entry = tk.Entry(top_frame, width=10)
        self.lane_entry.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="Count").grid(row=0, column=2, padx=5)
        self.vorodi_tedad_mashin = tk.Entry(top_frame, width=10)
        self.vorodi_tedad_mashin.insert(0, "1")
        self.vorodi_tedad_mashin.grid(row=0, column=3, padx=5)

        tk.Button(top_frame, text="Add Car", command=self.add_car).grid(row=0, column=4, padx=5)
        tk.Button(top_frame, text="Step", command=self.step_simulation).grid(row=0, column=5, padx=5)
        tk.Button(top_frame, text="Auto Run", command=self.toggle_auto_run).grid(row=0, column=6, padx=5)

        middle_frame = tk.Frame(self.root)
        middle_frame.pack(pady=10)

        self.canvas = tk.Canvas(middle_frame, width=500, height=500, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10)

        self.info_text = tk.Text(middle_frame, width=40, height=28)
        self.info_text.pack(side=tk.LEFT, padx=10)

    def add_car(self):
        lane_name = self.lane_entry.get().strip().lower()

        try:
            count = int(self.vorodi_tedad_mashin.get())
        except ValueError:
            messagebox.showerror("Error", "Count must be an integer")
            return

        if count <= 0:
            messagebox.showerror("Error", "Count must be greater than zero")
            return

        success = self.controller.add_car(lane_name, count)
        if not success:
            messagebox.showerror("Error", self.controller.akharin_vazeiat)

        self.update_view()

    def step_simulation(self):
        self.controller.step()
        self.update_view()

    def toggle_auto_run(self):
        self.auto_run = not self.auto_run
        if self.auto_run:
            self.run_auto()

    def run_auto(self):
        if self.auto_run:
            self.controller.step()
            self.update_view()
            self.root.after(700, self.run_auto)

    def draw_intersection(self):
        self.canvas.delete("all")

        self.canvas.create_rectangle(200, 0, 300, 500, fill="gray70", outline="")
        self.canvas.create_rectangle(0, 200, 500, 300, fill="gray70", outline="")

        self.canvas.create_line(250, 0, 250, 200, fill="white", dash=(8, 8), width=2)
        self.canvas.create_line(250, 300, 250, 500, fill="white", dash=(8, 8), width=2)
        self.canvas.create_line(0, 250, 200, 250, fill="white", dash=(8, 8), width=2)
        self.canvas.create_line(300, 250, 500, 250, fill="white", dash=(8, 8), width=2)

        mogheiat_cheragh = {
            "north": (220, 170),
            "south": (280, 330),
            "east": (330, 220),
            "west": (170, 280),
        }

        for lane_name, (x, y) in mogheiat_cheragh.items():
            color = self.intersection.lights[lane_name].color
            self.canvas.create_oval(x, y, x + 20, y + 20, fill=color)

        self.canvas.create_text(250, 60, text=f"North: {self.intersection.lanes['north'].tedad_mashin()}", font=("Arial", 12, "bold"))
        self.canvas.create_text(250, 440, text=f"South: {self.intersection.lanes['south'].tedad_mashin()}", font=("Arial", 12, "bold"))
        self.canvas.create_text(420, 250, text=f"East: {self.intersection.lanes['east'].tedad_mashin()}", font=("Arial", 12, "bold"))
        self.canvas.create_text(80, 250, text=f"West: {self.intersection.lanes['west'].tedad_mashin()}", font=("Arial", 12, "bold"))

    def update_info(self):
        text = ""
        text += f"Time: {self.controller.time}\n"
        text += f"Green Group: {self.controller.masir_sabz}\n"
        text += f"Remaining Green Time: {self.controller.time_sabz}\n"
        text += f"Total Waiting Cars: {self.controller.tedad_mashin_montazer()}\n"
        text += f"Total Passed Cars: {self.controller.tedad_mashin_radshode}\n"
        text += f"Average Waiting Time: {self.controller.miangir_entezar():.2f}\n"
        text += f"Last Status: {self.controller.akharin_vazeiat}\n\n"

        text += "Lane Details:\n"
        for lane_name in Name_masir:
            lane = self.intersection.lanes[lane_name]
            light = self.intersection.lights[lane_name]
            text += f"{lane_name}: cars={lane.tedad_mashin()}, light={light.color}\n"

        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, text)

    def update_view(self):
        self.draw_intersection()
        self.update_info()


if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficGUI(root)
    root.mainloop()
