import tkinter as tk
from tkinter import messagebox
import math

class Pendulum:
    def __init__(self, tool=140):
        self.tool = tool
        self.zavie = 0.05
        self.sorat_zavie = 0.0
        self.g = 9.81

    def update_vaziat(self, shatab_cart, dt):
        zavie_dot2 = (self.g / self.tool) * math.sin(self.zavie) - (shatab_cart / self.tool) * math.cos(self.zavie)
        self.sorat_zavie += zavie_dot2 * dt
        self.zavie += self.sorat_zavie * dt

    def oftade(self):
        return abs(self.zavie) > math.radians(45)

class Cart:
    def __init__(self, makan=400):
        self.makan = makan
        self.sorat = 0.0
        self.nirou = 0.0
        self.mass = 1.0

    def update_vaziat(self, dt):
        shatab = self.nirou / self.mass
        self.sorat += shatab * dt
        self.sorat *= 0.9
        self.makan += self.sorat * dt
        return shatab

class Simulation:
    def __init__(self, arz=800):
        self.arz = arz
        self.pendulum = Pendulum()
        self.cart = Cart(arz / 2)
        self.dt = 0.02
        self.game_over = False
        self.control_nirou = 0.0

    def reset(self):
        self.pendulum = Pendulum()
        self.cart = Cart(self.arz / 2)
        self.game_over = False
        self.control_nirou = 0.0

    def update_vaziat(self):
        if self.game_over:
            return

        self.cart.nirou = self.control_nirou
        shatab_cart = self.cart.update_vaziat(self.dt)
        self.pendulum.update_vaziat(shatab_cart, self.dt)

        if self.cart.makan < 50:
            self.cart.makan = 50
            self.cart.sorat = 0
        elif self.cart.makan > self.arz - 50:
            self.cart.makan = self.arz - 50
            self.cart.sorat = 0

        if self.pendulum.oftade():
            self.game_over = True

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bazi Taadoli Pendulum Maakoos (Manual)")
        self.root.geometry("900x650")
        self.sim = Simulation()
        self.frame_top = tk.Frame(root)
        self.frame_top.pack(pady=10)
        self.btn_reset = tk.Button(self.frame_top, text="Reset Bazi", width=15, command=self.reset_game, bg="lightblue")
        self.btn_reset.grid(row=0, column=0, padx=5)
        self.lbl_info = tk.Label(root, text="Control: Use Left/Right Arrow Keys to balance", font=("Arial", 12, "bold"), fg="darkred")
        self.lbl_info.pack(pady=5)
        self.canvas = tk.Canvas(root, width=800, height=500, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=10)
        self.lbl_status = tk.Label(root, text="Ba kelidha ye chap o rast pandoool ro negah dar!", font=("Arial", 11))
        self.lbl_status.pack(pady=5)
        self.root.bind("<Left>", self.key_left)
        self.root.bind("<Right>", self.key_right)
        self.root.bind("<KeyRelease-Left>", self.key_release)
        self.root.bind("<KeyRelease-Right>", self.key_release)
        self.loop()

    def reset_game(self):
        self.sim.reset()

    def key_left(self, event):
        self.sim.control_nirou = -120.0

    def key_right(self, event):
        self.sim.control_nirou = 120.0

    def key_release(self, event):
        self.sim.control_nirou = 0.0

    def rasm(self):
        self.canvas.delete("all")
        arz = 800
        zamin_y = 380
        self.canvas.create_line(0, zamin_y + 40, arz, zamin_y + 40, width=3, fill="black")
        cart_x = self.sim.cart.makan
        cart_y = zamin_y
        cart_w, cart_h = 80, 40
        self.canvas.create_rectangle(cart_x - cart_w / 2, cart_y - cart_h / 2, cart_x + cart_w / 2, cart_y + cart_h / 2, fill="skyblue", outline="black", width=2)
        self.canvas.create_oval(cart_x - 25, cart_y + 15, cart_x - 5, cart_y + 35, fill="black")
        self.canvas.create_oval(cart_x + 5, cart_y + 15, cart_x + 25, cart_y + 35, fill="black")
        pivot_x, pivot_y = cart_x, cart_y - cart_h / 2
        pend_len, zavie = self.sim.pendulum.tool, self.sim.pendulum.zavie
        bob_x = pivot_x + pend_len * math.sin(zavie)
        bob_y = pivot_y - pend_len * math.cos(zavie)
        self.canvas.create_line(pivot_x, pivot_y, bob_x, bob_y, width=4, fill="red")
        self.canvas.create_oval(bob_x - 12, bob_y - 12, bob_x + 12, bob_y + 12, fill="darkred")
        zavie_deg = math.degrees(self.sim.pendulum.zavie)
        self.canvas.create_text(140, 30, text=f"Zavie: {zavie_deg:.2f} deg", font=("Arial", 12, "bold"), fill="black")
        if self.sim.game_over:
            self.canvas.create_text(400, 200, text="Game Over! Pandoool Oftad", font=("Arial", 22, "bold"), fill="red")

    def loop(self):
        self.sim.update_vaziat()
        self.rasm()
        self.root.after(20, self.loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
