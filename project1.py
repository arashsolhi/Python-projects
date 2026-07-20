import tkinter as tk
from tkinter import messagebox

Tabaghat = 107
Zarfiat = 8


class Person:
    def __init__(self, Start_tabaghe, Tabaghe_maghsad, Darkhast):
        self.Start_tabaghe = Start_tabaghe
        self.Tabaghe_maghsad = Tabaghe_maghsad
        self.Darkhast = Darkhast

        if self.Tabaghe_maghsad > self.Start_tabaghe:
            self.Jahat_harkat = 1
        else:
            self.Jahat_harkat = -1

    def waiting_time(self, time):
        return time - self.Darkhast


class Floor:
    def __init__(self, number):
        self.number = number
        self.List_entezar = []

    def add_person(self, person):
        self.List_entezar.append(person)


class Elevator:
    def __init__(self, Zarfiat):
        self.Zarfiat = Zarfiat
        self.Magheiat = 1
        self.Jahat_harkat = 0
        self.List_dakhel_shode = []

    def is_full(self):
        return len(self.List_dakhel_shode) >= self.Zarfiat

    def add_passenger(self, person):
        if not self.is_full():
            self.List_dakhel_shode.append(person)
            return True
        return False

    def drop_off_passengers(self):
        List_kharjshode = []
        Savarnashode = []

        for person in self.List_dakhel_shode:
            if person.Tabaghe_maghsad == self.Magheiat:
                List_kharjshode.append(person)
            else:
                Savarnashode.append(person)

        self.List_dakhel_shode = Savarnashode
        return List_kharjshode


class Building:
    def __init__(self, Koletabaghat, Zarfiat):
        self.Koletabaghat = Koletabaghat
        self.List_koltabaghat = [Floor(i) for i in range(1, Koletabaghat + 1)]
        self.elevator = Elevator(Zarfiat)

    def get_floor(self, floor_number):
        return self.List_koltabaghat[floor_number - 1]


class Controller:
    def __init__(self, building):
        self.building = building
        self.time = 0
        self.List_savarshode = 0
        self.Vazeat = "System started"

    def add_request(self, Start_tabaghe, Tabaghe_maghsad, Darkhostmoshabeh=1):
        if Start_tabaghe == Tabaghe_maghsad:
            self.Vazeat = "Start and destination cannot be the same"
            return False

        if not (1 <= Start_tabaghe <= self.building.Koletabaghat):
            self.Vazeat = "Invalid start floor"
            return False

        if not (1 <= Tabaghe_maghsad <= self.building.Koletabaghat):
            self.Vazeat = "Invalid destination floor"
            return False

        floor = self.building.get_floor(Start_tabaghe)

        for _ in range(Darkhostmoshabeh):
            person = Person(Start_tabaghe, Tabaghe_maghsad, self.time)
            floor.add_person(person)

        self.Vazeat = f"Request added: {Darkhostmoshabeh} person(s) from {Start_tabaghe} to {Tabaghe_maghsad}"
        return True

    def has_pending_requests(self):
        if self.building.elevator.List_dakhel_shode:
            return True

        for floor in self.building.List_koltabaghat:
            if floor.List_entezar:
                return True

        return False

    def choose_direction(self):
        elevator = self.building.elevator

        if elevator.List_dakhel_shode:
            kharej_az_masir = True
            for person in elevator.List_dakhel_shode:
                if elevator.Jahat_harkat == 1 and person.Tabaghe_maghsad > elevator.Magheiat:
                    kharej_az_masir = False
                    break
                elif elevator.Jahat_harkat == -1 and person.Tabaghe_maghsad < elevator.Magheiat:
                    kharej_az_masir = False
                    break

            if kharej_az_masir:
                first_target = elevator.List_dakhel_shode[0].Tabaghe_maghsad
                if first_target > elevator.Magheiat:
                    elevator.Jahat_harkat = 1
                elif first_target < elevator.Magheiat:
                    elevator.Jahat_harkat = -1
                else:
                    elevator.Jahat_harkat = 0
            return

        nazdiktarin_darkhost = None
        fasele_ta_darkhast = 10**9

        for floor in self.building.List_koltabaghat:
            if floor.List_entezar:
                fasele_ta_tabaghe = abs(floor.number - elevator.Magheiat)
                if fasele_ta_tabaghe < fasele_ta_darkhast:
                    fasele_ta_darkhast = fasele_ta_tabaghe
                    nazdiktarin_darkhost = floor.number

        if nazdiktarin_darkhost is None:
            elevator.Jahat_harkat = 0
        elif nazdiktarin_darkhost > elevator.Magheiat:
            elevator.Jahat_harkat = 1
        elif nazdiktarin_darkhost < elevator.Magheiat:
            elevator.Jahat_harkat = -1
        else:
            floor = self.building.get_floor(elevator.Magheiat)
            if floor.List_entezar:
                elevator.Jahat_harkat = floor.List_entezar[0].Jahat_harkat
            else:
                elevator.Jahat_harkat = 0

    def pickup_passengers(self):
        elevator = self.building.elevator
        floor = self.building.get_floor(elevator.Magheiat)

        if not floor.List_entezar:
            return 0

        savarshode_hal = 0
        Savarnashode = []

        for person in floor.List_entezar:
            if elevator.is_full():
                Savarnashode.append(person)
                continue

            if elevator.Jahat_harkat == 0 or person.Jahat_harkat == elevator.Jahat_harkat:
                elevator.add_passenger(person)
                savarshode_hal += 1
            else:
                Savarnashode.append(person)

        floor.List_entezar = Savarnashode
        return savarshode_hal

    def step(self):
        self.time += 1
        elevator = self.building.elevator

        List_kharjshode = elevator.drop_off_passengers()
        self.List_savarshode += len(List_kharjshode)

        self.choose_direction()
        savarshode_hal = self.pickup_passengers()
        self.choose_direction()

        if elevator.Jahat_harkat == 1 and elevator.Magheiat < self.building.Koletabaghat:
            elevator.Magheiat += 1
            jahat_lahze = "moving up"
        elif elevator.Jahat_harkat == -1 and elevator.Magheiat > 1:
            elevator.Magheiat -= 1
            jahat_lahze = "moving down"
        else:
            jahat_lahze = "idle"

        self.Vazeat = (
            f"Time={self.time}, floor={elevator.Magheiat}, "
            f"dropped={len(List_kharjshode)}, picked={savarshode_hal}, status={jahat_lahze}"
        )

    def average_waiting_time(self):
        entezar_kol = 0
        total_people = 0

        for floor in self.building.List_koltabaghat:
            for person in floor.List_entezar:
                entezar_kol += person.waiting_time(self.time)
                total_people += 1

        for person in self.building.elevator.List_dakhel_shode:
            entezar_kol += person.waiting_time(self.time)
            total_people += 1

        if total_people == 0:
            return 0.0

        return entezar_kol / total_people

    def waiting_count(self):
        count = 0
        for floor in self.building.List_koltabaghat:
            count += len(floor.List_entezar)
        return count


class ElevatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Elevator Simulator")

        self.building = Building(Tabaghat, Zarfiat)
        self.controller = Controller(self.building)

        self.khodkar = False

        self.create_widgets()
        self.update_view()

    def create_widgets(self):
        panjere_bala = tk.Frame(self.root)
        panjere_bala.pack(pady=10)

        tk.Label(panjere_bala, text="Start Floor").grid(row=0, column=0, padx=5)
        self.namayeshgar_tabaghe = tk.Entry(panjere_bala, width=8)
        self.namayeshgar_tabaghe.grid(row=0, column=1, padx=5)

        tk.Label(panjere_bala, text="Destination").grid(row=0, column=2, padx=5)
        self.dest_entry = tk.Entry(panjere_bala, width=8)
        self.dest_entry.grid(row=0, column=3, padx=5)

        tk.Label(panjere_bala, text="Count").grid(row=0, column=4, padx=5)
        self.namayesh_tededmosafer = tk.Entry(panjere_bala, width=8)
        self.namayesh_tededmosafer.insert(0, "1")
        self.namayesh_tededmosafer.grid(row=0, column=5, padx=5)

        tk.Button(panjere_bala, text="Add Request", command=self.add_request).grid(row=0, column=6, padx=5)
        tk.Button(panjere_bala, text="Step", command=self.step_simulation).grid(row=0, column=7, padx=5)
        tk.Button(panjere_bala, text="Auto Run", command=self.toggle_auto_run).grid(row=0, column=8, padx=5)

        panjere_vasat = tk.Frame(self.root)
        panjere_vasat.pack(pady=10)

        self.canvas = tk.Canvas(panjere_vasat, width=220, height=700, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10)

        self.matni_etelat = tk.Text(panjere_vasat, width=45, height=40)
        self.matni_etelat.pack(side=tk.LEFT, padx=10)

    def add_request(self):
        try:
            Start_tabaghe = int(self.namayeshgar_tabaghe.get())
            Tabaghe_maghsad = int(self.dest_entry.get())
            Darkhostmoshabeh = int(self.namayesh_tededmosafer.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers")
            return

        if Darkhostmoshabeh <= 0:
            messagebox.showerror("Error", "Count must be greater than zero")
            return

        success = self.controller.add_request(Start_tabaghe, Tabaghe_maghsad, Darkhostmoshabeh)
        if not success:
            messagebox.showerror("Error", self.controller.Vazeat)

        self.update_view()

    def step_simulation(self):
        self.controller.step()
        self.update_view()

    def toggle_auto_run(self):
        self.khodkar = not self.khodkar
        if self.khodkar:
            self.run_auto()

    def run_auto(self):
        if self.khodkar:
            self.controller.step()
            self.update_view()
            self.root.after(500, self.run_auto)

    def draw_building(self):
        self.canvas.delete("all")

        ertefa = 700
        fasele_bala = 20
        margin_bottom = 20
        fasele_tabaghat = ertefa - fasele_bala - margin_bottom

        for shomare_rasm in range(1, Tabaghat + 1):
            y = ertefa - margin_bottom - ((shomare_rasm - 1) / (Tabaghat - 1)) * fasele_tabaghat

            if shomare_rasm % 10 == 0 or shomare_rasm == 1 or shomare_rasm == Tabaghat:
                self.canvas.create_text(20, y, text=str(shomare_rasm), font=("Arial", 8))
                self.canvas.create_line(40, y, 180, y, fill="#dddddd")

        shomare_feli = self.building.elevator.Magheiat
        y = ertefa - margin_bottom - ((shomare_feli - 1) / (Tabaghat - 1)) * fasele_tabaghat

        self.canvas.create_rectangle(100, y - 8, 150, y + 8, fill="blue")
        self.canvas.create_text(125, y, text="E", fill="white", font=("Arial", 10, "bold"))

    def update_info(self):
        elevator = self.building.elevator
        kol_montazer = self.controller.waiting_count()
        meiangin_entezar = self.controller.average_waiting_time()

        matn_jahat = "Idle"
        if elevator.Jahat_harkat == 1:
            matn_jahat = "Up"
        elif elevator.Jahat_harkat == -1:
            matn_jahat = "Down"

        matne_namayesh = []
        for floor in self.building.List_koltabaghat:
            if floor.List_entezar:
                matne_namayesh.append(f"Floor {floor.number}: {len(floor.List_entezar)} waiting")

        List_matn_dakhel = []
        for i, person in enumerate(elevator.List_dakhel_shode, start=1):
            List_matn_dakhel.append(
                f"Passenger {i}: {person.Start_tabaghe} -> {person.Tabaghe_maghsad}"
            )

        text = ""
        text += f"Time: {self.controller.time}\n"
        text += f"Current Floor: {elevator.Magheiat}\n"
        text += f"Direction: {matn_jahat}\n"
        text += f"Passengers in Elevator: {len(elevator.List_dakhel_shode)} / {elevator.Zarfiat}\n"
        text += f"Waiting People: {kol_montazer}\n"
        text += f"Served People: {self.controller.List_savarshode}\n"
        text += f"Average Waiting Time: {meiangin_entezar:.2f}\n"
        text += f"Last Action: {self.controller.Vazeat}\n\n"

        text += "Passengers Inside Elevator:\n"
        if List_matn_dakhel:
            text += "\n".join(List_matn_dakhel)
        else:
            text += "No passengers"
        text += "\n\n"

        text += "Floors With Waiting Requests:\n"
        if matne_namayesh:
            text += "\n".join(matne_namayesh[:30])
            if len(matne_namayesh) > 30:
                text += "\n..."
        else:
            text += "No waiting requests"

        self.matni_etelat.delete("1.0", tk.END)
        self.matni_etelat.insert(tk.END, text)

    def update_view(self):
        self.draw_building()
        self.update_info()


if __name__ == "__main__":
    root = tk.Tk()
    app = ElevatorGUI(root)
    root.mainloop()
