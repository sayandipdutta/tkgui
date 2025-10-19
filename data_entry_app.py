import tkinter as tk
from tkinter import ttk


class BoundText(tk.Text):
    def __init__(self, *args, textvariable: tk.Variable, **kwargs):
        super().__init__(*args, **kwargs)
        self.textvariable = textvariable
        self.insert("1.0", self.textvariable.get())
        self.textvariable.trace_add("write", self._set_content)
        self.bind("<<Modified>>", self._set_var)

    def _set_content(self, *_):
        """Update the content when the text variable is changed"""
        self.delete("1.0", tk.END)
        self.insert("1.0", self.textvariable.get())

    def _set_var(self, *_):
        """Update text variable when content is changed"""
        if self.edit_modified():
            content = self.get("1.0", "end-1chars")
            self.textvariable.set(content)
            self.edit_modified(False)


class LabeledInput(ttk.Frame):
    def __init__(
        self,
        parent,
        label,
        var: tk.Variable,
        input_cls=ttk.Entry,
        label_args=None,
        input_args=None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        label_args = label_args or {}
        input_args = input_args or {}
        self.variable = var
        self.variable.label_widget = self

        match input_cls:
            case ttk.Radiobutton:
                self.input = ttk.Frame(self)
                for v in input_args.pop("values", []):
                    button = input_cls(self.input, value=v, text=v, **input_args)
                    button.pack(side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill="x")
                self.label = None
            case ttk.Checkbutton | ttk.Button:
                input_args["text"] = label
                input_args["variable"] = self.variable
                self.input = input_cls(self, **input_args)
                self.label = None
            case _:
                self.label = ttk.Label(self, text=label, **label_args).grid(
                    row=0, column=0, sticky=tk.W + tk.E
                )
                input_args["textvariable"] = self.variable
                self.input = input_cls(self, **input_args)

        self.input.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.input.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.W + tk.E), **kwargs):
        super().grid(sticky=sticky, **kwargs)


class DataRecordForm(ttk.Frame):
    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self._vars = {
            "Date": tk.StringVar(),
            "Time": tk.StringVar(),
            "Technician": tk.StringVar(),
            "Lab": tk.StringVar(),
            "Plot": tk.StringVar(),
            "Seed Sample": tk.IntVar(),
            "Humidity": tk.DoubleVar(),
            "Light": tk.DoubleVar(),
            "Temperature": tk.DoubleVar(),
            "Equipment Fault": tk.BooleanVar(),
            "Plants": tk.IntVar(),
            "Blossoms": tk.IntVar(),
            "Fruit": tk.IntVar(),
            "Min Height": tk.DoubleVar(),
            "Max Height": tk.DoubleVar(),
            "Med Height": tk.DoubleVar(),
            "Notes": tk.StringVar(),
        }
        r_info = self._add_frame("Record Information", cols=3)

        LabeledInput(self, "Date", var=self._vars["Date"]).grid(row=0, column=0)
        LabeledInput(
            self,
            "Time",
            input_cls=ttk.Combobox,
            var=self._vars["Time"],
            input_args={"values": ["08:00", "12:00", "16:00", "20:00"]},
        ).grid(row=0, column=1)
        LabeledInput(self, "Technician", var=self._vars["Technician"]).grid(
            row=0, column=2
        )
        LabeledInput(
            r_info,
            "Lab",
            input_cls=ttk.Radiobutton,
            var=self._vars["Lab"],
            input_args={"values": ["A", "B", "C"]},
        ).grid(row=1, column=0)
        LabeledInput(
            r_info,
            "Plot",
            input_cls=ttk.Combobox,
            var=self._vars["Plot"],
            input_args={"values": list(range(1, 21))},
        ).grid(row=1, column=1)
        LabeledInput(r_info, "Seed Sample", var=self._vars["Seed Sample"]).grid(
            row=1, column=2
        )
        e_info = self._add_frame("Environment Data")

        LabeledInput(
            e_info,
            "Humidity (g/m³)",
            input_cls=ttk.Spinbox,
            var=self._vars["Humidity"],
            input_args={"from_": 0.5, "to": 52.0, "increment": 0.01},
        ).grid(row=0, column=0)
        LabeledInput(
            e_info,
            "Light (klx)",
            input_cls=ttk.Spinbox,
            var=self._vars["Light"],
            input_args={"from_": 0, "to": 100, "increment": 0.01},
        ).grid(row=0, column=1)
        LabeledInput(
            e_info,
            "Temperature (°C)",
            input_cls=ttk.Spinbox,
            var=self._vars["Temperature"],
            input_args={"from_": 4, "to": 40, "increment": 0.01},
        ).grid(row=0, column=2)
        LabeledInput(
            e_info,
            "Equipment Fault",
            input_cls=ttk.Checkbutton,
            var=self._vars["Equipment Fault"],
        ).grid(row=1, column=0, columnspan=3)
        p_info = self._add_frame("Plant Data")
        LabeledInput(
            p_info,
            "Plants",
            input_cls=ttk.Spinbox,
            var=self._vars["Plants"],
            input_args={"from_": 0, "to": 20},
        ).grid(row=0, column=0)
        LabeledInput(
            p_info,
            "Blossoms",
            input_cls=ttk.Spinbox,
            var=self._vars["Blossoms"],
            input_args={"from_": 0, "to": 1000},
        ).grid(row=0, column=1)
        LabeledInput(
            p_info,
            "Fruit",
            input_cls=ttk.Spinbox,
            var=self._vars["Fruit"],
            input_args={"from_": 0, "to": 1000},
        ).grid(row=0, column=2)
        LabeledInput(
            p_info,
            "Min Height (cm)",
            input_cls=ttk.Spinbox,
            var=self._vars["Min Height"],
            input_args={"from_": 0, "to": 1000, "increment": 0.01},
        ).grid(row=1, column=0)
        LabeledInput(
            p_info,
            "Max Height (cm)",
            input_cls=ttk.Spinbox,
            var=self._vars["Max Height"],
            input_args={"from_": 0, "to": 1000, "increment": 0.01},
        ).grid(row=1, column=1)
        LabeledInput(
            p_info,
            "Median Height (cm)",
            input_cls=ttk.Spinbox,
            var=self._vars["Med Height"],
            input_args={"from_": 0, "to": 1000, "increment": 0.01},
        ).grid(row=1, column=2)
        LabeledInput(
            self,
            "Notes",
            input_cls=BoundText,
            var=self._vars["Notes"],
            input_args={"width": 75, "height": 10},
        ).grid(sticky=tk.W, row=3, column=0)
        buttons = tk.Frame(self)
        buttons.grid(sticky=tk.W + tk.E, row=4)
        self.savebutton = ttk.Button(buttons, text="Save", command=self.master._on_save)
        self.savebutton.pack(side=tk.RIGHT)
        self.resetbutton = ttk.Button(buttons, text="Reset", command=self.reset)
        self.resetbutton.pack(side=tk.RIGHT)

    def _add_frame(self, label, cols=3):
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame

    def reset(self):
        """Resets the form entries"""
        for var in self._vars.values():
            if isinstance(var, tk.BooleanVar):
                var.set(False)
            else:
                var.set("")

    def get(self):
        data = dict()
        fault = self._vars["Equipment Fault"].get()
        for key, variable in self._vars.items():
            if fault and key in ("Light", "Humidity", "Temperature"):
                data[key] = ""
            else:
                try:
                    data[key] = variable.get()
                except tk.TclError:
                    message = f"Error in field: {key}. Data was not saved"
                    raise ValueError(message)
        return data


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ABQ Data Entry Application")
        self.columnconfigure(0, weight=1)
        ttk.Label(
            self, text="ABQ Data Entry Application", font=("TkDefaultFont", 16)
        ).grid(row=0)
        self.recordform = DataRecordForm(self)
        self.recordform.grid(row=1, padx=10, sticky=(tk.W + tk.E))
        self.status = tk.StringVar()
        ttk.Label(self, textvariable=self.status).grid(
            sticky=(tk.W + tk.E), row=2, padx=10
        )
        self._records_saved = 0

    def _on_save(self):
        """Handles save button clicks"""
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "abq_data_record_{}.csv".format(datestring)
        newfile = not Path(filename).exists()
        try:
            data = self.recordform.get()
        except ValueError as e:
            self.status.set(str(e))
            return
        with open(filename, "a", newline="") as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)
        self._records_saved += 1
        self.status.set("{} records saved this session".format(self._records_saved))
        self.recordform.reset()


if __name__ == "__main__":
    import csv
    from datetime import datetime
    from pathlib import Path

    app = Application()
    app.mainloop()
