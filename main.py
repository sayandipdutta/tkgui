import tkinter as tk
from typing import no_type_check


root = tk.Tk()

root.title("Banana interest survey")
root.geometry("640x480+300+300")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Please take the survey",
    font="Arial 16 bold",
    background="brown",
    foreground="#FF0",
)

name_label = tk.Label(root, text="What is your name?")
name_input = tk.Entry(root)
eater_input = tk.Checkbutton(root, text="Are you a banana eater?")
num_label = tk.Label(root, text="How many bananas do you eat?")
num_input = tk.Spinbox(root, from_=1, to=10, increment=1)
color_label = tk.Label(root, text="What is the best color for a banana?")
color_input = tk.Listbox(root, height=1)

color_choices = ("Any", "Yellow", "Yellow-Green", "Green", "Brown")
for choice in color_choices:
    color_input.insert(tk.END, choice)

submit_btn = tk.Button(root, text="Submit Survey")

output_line = tk.Label(root, text="", anchor="w", justify="left")

title.grid(columnspan=2)
name_label.grid(row=1, column=0)
name_input.grid(row=1, column=1)
eater_input.grid(row=2, columnspan=3, sticky=tk.W + tk.E)
num_label.grid(row=3, sticky=tk.W)
num_input.grid(row=3, column=1, columnspan=2, sticky=tk.W + tk.E)
color_label.grid(row=4, columnspan=2, sticky=tk.W, pady=10)
color_input.grid(row=5, columnspan=2, sticky=tk.W + tk.E, padx=25)

submit_btn.grid(row=99)
output_line.grid(row=100)

_ = root.columnconfigure(1, weight=1)
_ = root.rowconfigure(99, weight=2)
_ = root.rowconfigure(100, weight=1)


@no_type_check
def on_submit():
    name = name_input.get()
    number = num_input.get()
    color = (
        color_input.get(selected_index)
        if (selected_index := color_input.curselection())
        else ""
    )
    message = f"Hi, {name}. You eat {number} {color} bananas."
    output_line.configure(text=message)


res = submit_btn.configure(command=on_submit)
print(res)

if __name__ == "__main__":
    root.mainloop()
