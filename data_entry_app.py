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
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self, *args, **kwargs)
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

    def _add_frame(self, label, cols=3):
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame
