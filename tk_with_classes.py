import tkinter as tk
from tkinter import ttk
import json


class JSONVar(tk.StringVar):
    def __init__(self, *args, **kwargs):
        kwargs["value"] = json.dumps(kwargs.get("value"))
        super().__init__(*args, **kwargs)

    def set(self, value, *args, **kwargs):
        string = json.dumps(value)
        super().set(string, *args, **kwargs)

    def get(self, *args, **kwargs):
        string = super().get(*args, **kwargs)
        return json.loads(string)


class LabelInput(ttk.Frame):
    def __init__(self, master, label, input_cls, input_kwargs, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.label = ttk.Label(self, text=label, anchor="w")
        self.input = input_cls(self, **input_kwargs)
        self.columnconfigure(1, weight=1)
        self.label.grid(sticky=tk.E + tk.W)
        self.input.grid(row=0, column=1, sticky=tk.E + tk.W)


if __name__ == "__main__":
    root = tk.Tk()
    var1 = JSONVar(root)
    var1.set([1, 2, 3])
    print(var1.get()[1])

    labin = LabelInput(
        root,
        label="Your name",
        input_cls=ttk.Entry,
        input_kwargs={"background": "yellow"},
    )
    labin.grid()

    root.mainloop()
