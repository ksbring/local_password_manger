import json
import random
import tkinter as tk
import pyperclip
from tkinter import messagebox

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generator():
    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)
    random.shuffle(password_list)

    secure_password = "".join(password_list)
    pass_in.delete(0, tk.END)
    pass_in.insert(0, secure_password)

    pyperclip.copy(secure_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    ws = website_in.get()
    em = email_in.get()
    ps = pass_in.get()
    new_dict = {
        ws: {
            "email": em,
            "password": ps
        }
    }
    if len(ws) < 1 or len(ps) < 1 or len(em) < 1:
        messagebox.showerror(title="Error!", message="Please fill all the fields.")
    else:
        is_okay = messagebox.askokcancel(title=ws, message=f"These are the details entered: \nEmail: {em}"
                                                           f"\nPassword: {ps}\nProceed?")
        if is_okay:
            try:
                with open("data.json", mode="r") as file:
                    data = json.load(file)
                    data.update(new_dict)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = new_dict

            with open("data.json", mode="w") as file:
                json.dump(data, file, indent=4)

            website_in.delete(0, tk.END)
            pass_in.delete(0, tk.END)
            email_in.delete(0, tk.END)
            email_in.insert(0, "jeonamorh@hotmail.com")
            website_in.focus()


# --------------------------- SEARCHER ---------------------------------#

def searcher():
    ws = website_in.get()
    try:
        with open("data.json", mode="r") as pw_file:
            passes = json.load(pw_file)
            my_pass = passes[ws]["password"]
            my_email = passes[ws]["email"]
            messagebox.showinfo(title=ws, message=f"Email: {my_email}\n"
                                                  f"Password: {my_pass}\n\n"
                                                  f"Password has been copied to your"
                                                  f" clipboard.")
            pyperclip.copy(my_pass)
    except FileNotFoundError:
        messagebox.showerror(title="Error!", message="No data file found.")

    except KeyError:
        messagebox.showinfo(title="Error!", message=f"No data found for {ws}.")


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tk.Canvas(width=200, height=200)
img = tk.PhotoImage(file="logo.png")
canvas.create_image((100, 100), image=img)
canvas.grid(row=0, column=1)
# Label
web_site = tk.Label(text="Website:")
web_site.grid(row=1, column=0)
email = tk.Label(text="Email/Username:")
email.grid(row=2, column=0)
password = tk.Label(text="Password:")
password.grid(row=3, column=0)
# Entry
website_in = tk.Entry()
website_in.grid(row=1, column=1, sticky="EW")
website_in.focus()
email_in = tk.Entry()
email_in.grid(row=2, column=1, columnspan=2, sticky="EW")
email_in.insert(0, "jeonamorh@hotmail.com")
pass_in = tk.Entry()
pass_in.grid(row=3, column=1, sticky="EW")
# Button
search = tk.Button(text="Search", command=searcher)
search.grid(row=1, column=2, sticky="EW")
generate_pass = tk.Button(text="Generate Password", command=generator)
generate_pass.grid(row=3, column=2, sticky="EW")
add_button = tk.Button(text="Add", width=35, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
