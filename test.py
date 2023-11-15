import tkinter as tk


def on_click():
    if checkbutton_var.get() == 1:
        additional_section.pack(pady = 10, fill = tk.X)
    elif checkbutton_var.get() == 0:
        additional_section.pack_forget()


root = tk.Tk()
root.title("Registration Form")
 
main_frame = tk.Frame(root)
main_frame.pack(pady=10)
 
name_label = tk.Label(main_frame, text="Name:")
name_label.grid(row=0, column=0, sticky="W", padx = (10, 5))
 
name_entry = tk.Entry(main_frame)
name_entry.grid(row=0, column=1, padx = (5, 10))
 
email_label = tk.Label(main_frame, text="Email:")
email_label.grid(row=1, column=0, sticky="W", padx = (10, 5))
 
email_entry = tk.Entry(main_frame)
email_entry.grid(row=1, column=1, padx = (5, 10))
 
checkbutton_var = tk.IntVar()
checkbutton = tk.Checkbutton(main_frame, text="Optional Details", 
                             variable=checkbutton_var, command=on_click)
checkbutton.grid(row=2, column=0, sticky="W", padx=(10,5), pady=(10,5))
 
### Additional Fields
additional_section = tk.Frame(root)
 
age_label = tk.Label(additional_section, text="Email")
age_label.grid(row=0, column=0, sticky="W", padx = (10, 10))
 
age_entry = tk.Entry(additional_section)
age_entry.grid(row=0, column=1)
 
gender_label = tk.Label(additional_section, text="Address")
gender_label.grid(row=1, column=0, sticky="W", padx = (10, 10))
 
gender_entry = tk.Entry(additional_section)
gender_entry.grid(row=1, column=1)
 
root.mainloop()