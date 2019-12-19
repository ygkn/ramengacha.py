from tkinter import ttk
import tkinter as tk
from random import choice

from filter_shops import filter_shops
from get_ramenshop import get_ramenshop

locations = {
    "BKC": {"lat": 34.9787739, "lng": 135.9705647},
    "衣笠": {"lat": 35.0333103, "lng": 135.7242294},
    "OIC": {"lat": 34.8095351, "lng": 135.5590796},
}

colors = {"BKC": "#bedaf2", "衣笠": "#f6bde0", "OIC": "#b6df5d"}

w_height = 600
w_width = 400
w_border = 50


root = tk.Tk()
root.title("立命館周辺ラーメンガチャ")
root.geometry(f"{int(w_width)}x{int(w_height)}")
root.resizable(0, 0)

style = ttk.Style()


style.theme_settings(
    "default",
    {
        "Result.TLabel": {
            "configure": {
                "font": ("System", 16),
                "width": 20,
                "background": "#ffffff",
                "padding": 16,
                "pady": 20,
                "anchor": "c",
                "relief": "solid",
                "borderwidth": 1,
            }
        },
        "TButton": {
            "configure": {"relief": "solid", "borderwidth": 1, "background": "#ffffff"}
        },
        "TFrame": {"configure": {"background": "#ffffff"}},
        "TLabel": {"configure": {"borderwidth": 0, "background": "#ffffff"}},
        "TSpinbox": {
            "configure": {"relief": "solid", "borderwidth": 1, "background": "#ffffff"}
        },
        "TEntry": {
            "configure": {
                "relief": "solid",
                "borderwidth": 1,
                "background": "#ffffff",
            },
        },
        "TMenubutton": {
            "configure": {
                "relief": "solid",
                "borderwidth": 1,
                "background": "#ffffff",
                "width": 4,
            }
        },
    },
)


class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(
            master,
            style="App.TFrame",
            width=w_width - w_border * 2,
            height=w_height - w_border * 2,
        )
        self.master = master

        self.turing = False
        self.showing = None
        self.ramenlist = []
        self.campus = tk.StringVar(self, value="BKC")
        self.radius = tk.StringVar(self, value="4000")
        self.min_rate = tk.StringVar(self, value="0")
        self.max_rate = tk.StringVar(self, value="5")
        self.result = tk.StringVar(self, value="???")
        self.button_text = tk.StringVar(self, value="GO!")
        self.create_widgets()
        self.set_color("BKC")

    def create_widgets(self):
        self.bg = tk.Canvas(self.master, width=w_width, height=w_height)
        self.bg.place(x=0, y=0)
        self.place(x=w_border, y=w_border)
        self.lift()

        Logo(self).grid(sticky=tk.W + tk.E)
        Campus(self, self.campus, ["衣笠", "BKC", "OIC"], command=self.set_color).grid(
            padx=10, pady=10, sticky=tk.W + tk.E
        )
        Distance(self, self.radius).grid(padx=10, pady=10, sticky=tk.W + tk.E)
        Rate(self, self.min_rate, self.max_rate).grid(
            padx=10, pady=10, sticky=tk.W + tk.E
        )
        ttk.Button(
            self, textvariable=self.button_text, command=self.button_pushed
        ).grid(padx=10, pady=10, sticky=tk.W + tk.E)
        Result(self, self.result).grid(padx=10, pady=10, sticky=tk.W + tk.E)

    def fetch_shoplist(self):
        self.ramenlist = filter_shops(
            get_ramenshop(locations.get(self.campus.get()), int(self.radius.get())),
            False,
            int(self.min_rate.get()),
            int(self.max_rate.get()),
        )

    def button_pushed(self):
        if not self.turing:
            self.button_text.set("SEARCHING SHOPS...")
            self.fetch_shoplist()
            self.turing = True
            self.button_text.set("STOP")
            self.slot()
        else:
            self.turing = False
            self.button_text.set("GO")

    def slot(self):
        self.showing = choice(self.ramenlist)
        self.result.set(self.showing["name"])
        if self.turing:
            self.master.after(100, self.slot)

    def set_color(self, campus):
        self.bg.create_rectangle(0, 0, w_width, w_height, fill=colors.get(campus))

        radius = 16
        x1 = w_border - radius
        y1 = w_border - radius
        x2 = w_width - x1
        y2 = w_height - y1

        points = [
            x1 + radius,
            y1,
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]

        self.bg.create_polygon(points, smooth=True, fill="#fff")


class Logo(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.image = tk.PhotoImage(file="logo.png")
        self.create_widgets()

    def create_widgets(self):
        self.logo = tk.Canvas(
            self, width=300, height=147, background="#fff", highlightthickness=0,
        )
        self.logo.create_image(0, 0, image=self.image, anchor=tk.NW)

        self.logo.grid()


class Campus(ttk.Frame):
    def __init__(self, master=None, value=None, options=[], command=None):
        super().__init__(master, style="Campus.TFrame")
        self.value = value
        self.options = options
        self.command = command
        self.create_widgets()

    def create_widgets(self):
        self.campus_option = ttk.OptionMenu(
            self, self.value, "", *self.options, command=self.command
        )
        self.campus_option.pack(side=tk.LEFT)
        self.after_text = ttk.Label(self, text="から")
        self.after_text.pack(side=tk.LEFT)


class Distance(ttk.Frame):
    def __init__(self, master=None, radius=None, style="Distance.TFrame"):
        super().__init__(master)
        self.radius = radius
        self.create_widgets()

    def create_widgets(self):
        self.radius_spinbox = ttk.Spinbox(
            self, width=5, textvariable=self.radius, from_=0, to=99999, increment=1
        )
        self.radius_spinbox.pack(side=tk.LEFT)
        self.label2 = ttk.Label(self, text="m 圏内の")
        self.label2.pack(side=tk.LEFT)


class Rate(ttk.Frame):
    def __init__(self, master=None, min_rate=None, max_rate=None):
        super().__init__(master)
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.create_widgets()

    def create_widgets(self):
        self.label3 = ttk.Label(self, text="Google Maps の評価が")
        self.label3.pack(side=tk.LEFT)
        self.min_rate_spinbox = ttk.Spinbox(
            self, width=1, textvariable=self.min_rate, from_=0, to=5, increment=1
        )
        self.min_rate_spinbox.pack(side=tk.LEFT)
        self.label4 = ttk.Label(self, text="以上")
        self.label4.pack(side=tk.LEFT)
        self.max_rate_spinbox = ttk.Spinbox(
            self, width=1, textvariable=self.max_rate, from_=0, to=5, increment=1
        )
        self.max_rate_spinbox.pack(side=tk.LEFT)
        self.label5 = ttk.Label(self, text="以下")
        self.label5.pack(side=tk.LEFT)


class Result(ttk.Frame):
    def __init__(self, master=None, result=None):
        super().__init__(master, style="Result.TFrame")
        self.result = result
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, textvariable=self.result, style="Result.TLabel")
        label.pack()


app = App(master=root)
app.mainloop()
