from tkinter import *
from tkinter import ttk, messagebox
import torch
import torch.nn as nn
from torch.utils.data import Dataset
import random

class SurvivedModel(nn.Module):
    def __init__(self, MAXLENGTH=1000):
        super(SurvivedModel, self).__init__()
        self.layer1 = nn.Linear(MAXLENGTH, 48)
        self.layer2 = nn.Linear(48, 1)
        self.sigmoid = nn.Sigmoid()
        pass

    def forward(self, x):
        x = self.sigmoid(self.layer1(x))
        x = self.layer2(x)
        x = self.sigmoid(x)
        return x
    
class TitanicSurvivalDatasetTest(Dataset):
    def __init__(self, test_tensor: torch.Tensor):
        self.data = test_tensor

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data.data[index]

# functions for converting data
MAXLENGTH = 1000

def add_padding(list_item, max=500):
    result = list_item
    while len(result) < max:
        result.append(0)
    return result

def input_to_ascii(train_list):
    result = []
    for train in train_list:
        # print(train)
        temp = []
        for i, item in enumerate(train):
            current_item = []
            # print(i, item)
            if (i != 2):
                for char in item:
                    current_item.append(ord(char))
                
                current_item = add_padding(current_item, 40)
            else:
                for char in item:
                    current_item.append(ord(char))
                current_item = add_padding(current_item, 250)
            current_item.append(-1)
            temp = temp + current_item
        add_padding(temp, MAXLENGTH)
        result.append(temp)
    return result

# used to set the minimum threshold
# makes the output to be either on or 0 based on the threshold
def binary_output(output, minimum_threshold = 0.5):
    return True if (output>minimum_threshold) else False

# loads the ai model and evaluates the input of the user
# returns a Boolean of whether the user survived or not
def inference(user_input: list) -> bool:
    path_to_model = "machine-learning\Kaggle\pytorch\Titanic - Machine Learning from Disaster\survived_model(0.77033).pt"
    survived_ai_model: SurvivedModel = torch.load(path_to_model)
    
    input = input_to_ascii([user_input])
    input_tensor = torch.FloatTensor(input)
    input_dataset = TitanicSurvivalDatasetTest(input_tensor)

    # start the inference
    survived_ai_model.eval()

    output: torch.Tensor = survived_ai_model(input_dataset.data)

    return binary_output(output.item(), 0.5)


def on_save():
    # Check if all fields are filled
    # Dropdowns are not checked as they have default selection
    if not (
            name_entry.get()
            and age.get()
            and sibling_spouses.get()
            and parents_children.get()
            and ticket_number.get()
            and fare.get()):
        messagebox.showerror("Error", "Please fill all fields")
        return

    # Fetch values from all fields
    name = name_entry.get()

    passenger_class_value = passenger_class_dropdown.get()
    passenger_class = passenger_class_value[0]  # get first char

    sex_value = sex_dropdown.get()
    sex = sex_value.lower()  # lowercase

    age_value = age.get()
    sibling_spouses_value = sibling_spouses.get()
    parents_children_value = parents_children.get()
    ticket_number_value = ticket_number.get()
    fare_value = fare.get()

    embark_value = embark_dropdown.get()
    embark = embark_value[0]  # get first char

    print("-" * 20)
    print("Name:", name)
    print("Passenger Class:", passenger_class)
    print("Sex:", sex)
    print("Age:", age_value)
    print("Siblings/Spouses:", sibling_spouses_value)
    print("Parents/Children:", parents_children_value)
    print("Ticket Number:", ticket_number_value)
    print("Fare:", fare_value)
    print("Embark Point:", embark)
    print("-" * 20)

    
    user_input = []

    # unnecessary value that is needed for my model
    # magic number because of unclean training data
    passenger_id = random.randint(892, 1309)
    user_input.append(str(passenger_id))
    user_input.append(str(passenger_class))
    user_input.append(str(name))
    user_input.append(str(sex))
    user_input.append(str(age))
    user_input.append(str(sibling_spouses_value))
    user_input.append(str(parents_children_value))
    user_input.append(str(ticket_number_value))
    user_input.append(str(fare_value))
    user_input.append(str(''))
    user_input.append(str(embark))
    
    status = inference(user_input)

    # Update Survival Status label text
    survival_status.config(text=f"Survival Status: {"ALIVE" if status else "DEAD"}")


def restrict_to_number(event):
    v = event.char
    try:
        v = int(v)
    except ValueError:
        if v != "\x08" and v != "":
            return "break"


def restrict_to_float(event):
    v = event.char

    # Allow digits 0-9, decimal point (.), and backspace (\x08)
    if v.isdigit() or v == "." or v == "\x08":
        # Check if trying to delete with backspace
        if v == "\x08":
            return  # Allow the deletion by not returning "break"

        # Check if trying to add a decimal point
        if v == ".":
            # Ensure only one decimal point is allowed
            if "." in event.widget.get():
                return "break"

        # Ensure the input is valid as a number
        try:
            float(event.widget.get() + v)  # Try to convert to float
        except ValueError:
            return "break"
    else:
        return "break"  # Prevent any other characters from being entered


if __name__ == "__main__":
    window = Tk()

    WINDOW_HEIGHT = 600
    WINDOW_WIDTH = 320

    ENTRY_WIDTH = 20
    COMBOBOX_WIDTH = 17

    # Calculate position to center the window on the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2

    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    window.title("Test GUI")
    window.config(background="#403075")

    icon = PhotoImage(file='user.png')
    window.iconphoto(TRUE, icon)

    title = Label(window,
                text="Titanic Survival Guesser",
                font=("Century Gothic", 18, "bold", "italic"),
                fg="white",
                bg="#403075")
    title.grid(row=0, column=0, columnspan=2, pady=(20, 10))  # Adding padding to the top and bottom

    # Passenger Ticket Class
    Label(window, text="Ticket Class:", bg="#403075", fg="white").grid(row=1, column=0, padx=20, pady=5, sticky='w')
    passenger_class_options = ["1st Class", "2nd Class", "3rd Class"]
    passenger_class_dropdown = ttk.Combobox(window, values=passenger_class_options, state="readonly", width=COMBOBOX_WIDTH)
    passenger_class_dropdown.current(2)
    passenger_class_dropdown.grid(row=1, column=1, padx=20, pady=5, sticky='w')

    # Passenger Name
    Label(window, text="Name:", bg="#403075", fg="white").grid(row=2, column=0, padx=20, pady=5, sticky='w')
    name_entry = Entry(window, width=ENTRY_WIDTH)
    name_entry.grid(row=2, column=1, padx=20, pady=5, sticky='w')

    # Passenger Sex
    Label(window, text="Sex:", bg="#403075", fg="white").grid(row=3, column=0, padx=20, pady=5, sticky='w')
    sex_options = ["Male", "Female"]
    sex_dropdown = ttk.Combobox(window, values=sex_options, state="readonly", width=COMBOBOX_WIDTH)
    sex_dropdown.current(0)
    sex_dropdown.grid(row=3, column=1, padx=20, pady=5, sticky='w')

    # Passenger Age
    Label(window, text="Age:", bg="#403075", fg="white").grid(row=4, column=0, padx=20, pady=5, sticky='w')
    age = Entry(window, width=ENTRY_WIDTH)
    age.grid(row=4, column=1, padx=20, pady=5, sticky='w')
    age.bind('<Key>', restrict_to_number)

    # Number of Siblings and Spouses
    Label(window, text="Siblings/Spouses:", bg="#403075", fg="white").grid(row=5, column=0, padx=20, pady=5, sticky='w')
    sibling_spouses = Entry(window, width=ENTRY_WIDTH)
    sibling_spouses.grid(row=5, column=1, padx=20, pady=5, sticky='w')
    sibling_spouses.bind('<Key>', restrict_to_number)

    # Number of Parents and Children
    Label(window, text="Parents/Children:", bg="#403075", fg="white").grid(row=6, column=0, padx=20, pady=5, sticky='w')
    parents_children = Entry(window, width=ENTRY_WIDTH)
    parents_children.grid(row=6, column=1, padx=20, pady=5, sticky='w')
    parents_children.bind('<Key>', restrict_to_number)

    # Ticket Number
    Label(window, text="Ticket Number:", bg="#403075", fg="white").grid(row=7, column=0, padx=20, pady=5, sticky='w')
    ticket_number = Entry(window, width=ENTRY_WIDTH)
    ticket_number.grid(row=7, column=1, padx=20, pady=5, sticky='w')
    ticket_number.bind('<Key>', restrict_to_number)

    # Passenger Fare
    Label(window, text="Fare:", bg="#403075", fg="white").grid(row=8, column=0, padx=20, pady=5, sticky='w')
    fare = Entry(window, width=ENTRY_WIDTH)
    fare.grid(row=8, column=1, padx=20, pady=5, sticky='w')
    fare.bind('<Key>', restrict_to_float)

    # Embarkation Point
    Label(window, text="Embarkation Point:", bg="#403075", fg="white").grid(row=9, column=0, padx=20, pady=5, sticky='w')
    embark_options = ["Cherbourg", "Queenstown", "Southampton"]
    embark_dropdown = ttk.Combobox(window, values=embark_options, state="readonly", width=COMBOBOX_WIDTH)
    embark_dropdown.current(0)
    embark_dropdown.grid(row=9, column=1, padx=20, pady=5, sticky='w')

    # Save Button
    button = Button(window, text="Start", command=on_save, padx=20, font=("Century Gothic", 10))
    button.grid(row=10, column=0, columnspan=2, pady=(20, 10))

    # Survival Status
    survival_status = Label(window,
                            text="Survival Status: ",
                            font=("Century Gothic", 16, "bold", "italic"),
                            bg="#403075",
                            fg="white"
                            )
    survival_status.grid(row=11, column=0, columnspan=2, pady=(20, 10))

    window.resizable(False, False)
    window.mainloop()
