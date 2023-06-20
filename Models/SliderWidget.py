import tkinter as tk
from tkinter import messagebox

class SliderWidget:
    def __init__(self, arg_window: "tk.Tk()", arg_title: str, arg_min: float, arg_max: float, arg_resolution: float,
                 arg_initial_value: float, arg_row: int, arg_column: int):
        # Initialize the SliderWidget object with the provided arguments
        self.window = arg_window
        self.title = arg_title
        self.minimum = arg_min
        self.maximum = arg_max
        self.resolution = arg_resolution
        self.initial_value = arg_initial_value
        self.row = arg_row
        self.column = arg_column
        self.last_slider_value = self.initial_value
        self.return_value = self.initial_value
        self.state = True

    def create(self):
        def state_false():
            # Set the state of the slider to False
            self.state = False

        def update_values(arg_text_entry):
            # Update the slider value and the associated text entry
            self.last_slider_value = slider.get()
            arg_text_entry.delete(0, tk.END)
            arg_text_entry.insert(0, self.last_slider_value)

        # Create a text entry widget
        text_entry = tk.Entry(self.window, width=8)
        text_entry.grid(row=self.row, column=self.column + 1)

        # Create a label for the slider
        label_title = tk.Label(self.window, text=self.title)
        label_title.grid(row=self.row, column=self.column)

        # Create a slider widget
        slider = tk.Scale(self.window, from_=self.minimum, to=self.maximum, resolution=self.resolution, sliderlength=15,
                          length=200, orient=tk.HORIZONTAL,
                          command=lambda value: [state_false(), update_values(text_entry)])

        slider.grid(row=self.row, column=self.column + 2)
        slider.configure(showvalue=False)

        # Set the initial value of the slider
        slider.set(self.initial_value)

        def update_from_entry(event=None):
            # Update the slider value when the Enter key is pressed in the text entry
            value = text_entry.get()
            try:
                value = int(value)
                if self.minimum <= value <= self.maximum:
                    slider.set(value)
                else:
                    raise ValueError
            except ValueError:
                text_entry.delete(0, tk.END)
                text_entry.insert(0, str(slider.get()))

        # Bind the text entry to the update_from_entry function
        text_entry.bind("<Return>", update_from_entry)

    def confirm(self):
        # Set the return value of the slider to the last slider value
        self.return_value = self.last_slider_value
