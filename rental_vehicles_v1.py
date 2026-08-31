import tkinter as tk
from tkinter import messagebox
from collections import Counter
import mysql.connector

def extract_id_number(string):
    values = string.split(',')
    for value in values:
        if "ID" in value:
            id_number = int(value.split(':')[1].strip())
            return id_number

class RentalVehicleApp:
    def validate_numbers_only(self, text_input):
        if text_input.isdigit() or text_input == "":
            return True
        else:
            return False

    def __init__(self, root):

        self.root = root
        self.root.title("Rental Vehicle Agency Management")

        window_width = 700
        window_height = 600


        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()


        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))


        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        # -----------------------------------------------------------

        vcmd_numbers = (self.root.register(self.validate_numbers_only), '%P')


        self.db_config =  {
            'user': 'root',
            'password': 'Losvengadores12#',
            'host': 'localhost',
            'database': 'rent_a_car'
        }

        self.connection = mysql.connector.connect(**self.db_config)
        self.cursor = self.connection.cursor()

        #Frames

        self.main_container = tk.Frame(self.root)
        self.main_container.pack(expand=True)

        self.form_frame = tk.Frame(self.main_container)
        self.form_frame.pack(pady=8)

        self.details_frame=tk.Frame(self.form_frame)
        self.details_frame.pack(pady=8)

        self.fuel_frame=tk.Frame(self.form_frame)
        self.fuel_frame.pack(pady=8)

        self.avail_frame=tk.Frame(self.form_frame)
        self.avail_frame.pack(pady=8)

        self.save_btn = tk.Button(self.form_frame, text="Save Vehicle", command=self.add_rental_vehicle, bg="lightgreen")
        self.save_btn.pack(pady=10)

        self.btn_frame=tk.Frame(self.main_container)
        self.btn_frame.pack(pady=8)

        self.back_btn = tk.Button(self.form_frame, text="Back to Menu", command=self.return_to_menu, bg="lightcoral")
        self.back_btn.pack(pady=5)


        #Vehicle's details
        self.make_label = tk.Label(self.details_frame, text="Vehicle's Make:", font=("Times New Roman", 12))
        self.make_label.grid(row=0, column= 0, padx=5, pady=5)
        self.make_entry = tk.Entry(self.details_frame)
        self.make_entry.grid(row=1, column= 0, padx=5, pady=5)

        self.model_label = tk.Label(self.details_frame, text="Vehicle's Model:", font=("Times New Roman", 12))
        self.model_label.grid(row=0, column= 1, padx=5, pady=5)
        self.model_entry = tk.Entry(self.details_frame)
        self.model_entry.grid(row=1, column= 1, padx=5, pady=5)

        self.daily_tariff_label=tk.Label(self.details_frame, text="Vehicle's Daily Tariff:", font=("Times New Roman", 12))
        self.daily_tariff_label.grid(row=0, column=2, padx=5, pady=5)
        self.daily_tariff_entry = tk.Entry(self.details_frame, validate='key', validatecommand=vcmd_numbers)
        self.daily_tariff_entry.grid(row=1, column=2, padx=5, pady=5)

        self.year_label = tk.Label(self.details_frame, text="Vehicle's Year:", font=("Times New Roman", 12))
        self.year_label.grid(row=0, column=3, padx=5, pady=5)
        self.year_entry = tk.Entry(self.details_frame, validate='key', validatecommand=vcmd_numbers)
        self.year_entry.grid(row=1, column=3, padx=0, pady=5)

        #Vehicle's fuel
        self.fuel_var=tk.StringVar()
        self.fuel_var.set(" ")

        self.fuel_label= tk.Label(self.fuel_frame, text="Choose the vehicle's fuel:", font=("Times New Roman", 12))
        self.fuel_label.grid(row=0, column=0, padx=5, pady=5)

        self.radio_gasoline=tk.Radiobutton(self.fuel_frame, text="Gasoline", variable=self.fuel_var, value="Gasoline")
        self.radio_gasoline.grid(row=0, column=1, padx=5, pady=5)
        self.radio_diesel= tk.Radiobutton(self.fuel_frame, text="Diesel", variable=self.fuel_var, value="Diesel")
        self.radio_diesel.grid(row=0, column=2, padx=5, pady=5)
        self.radio_electric= tk.Radiobutton(self.fuel_frame, text="Electric", variable=self.fuel_var, value="Electric")
        self.radio_electric.grid(row=0, column=3, padx=5, pady=5)
        self.radio_hybrid= tk.Radiobutton(self.fuel_frame, text="Hybrid", variable=self.fuel_var, value="Hybrid")
        self.radio_hybrid.grid(row=0, column=4, padx=5, pady=5)

        #Vehicle's availability
        self.avail_var=tk.BooleanVar(value=True)


        self.avail_label=tk.Label(self.avail_frame, text="Choose the vehicle's availability:", font=("Times New Roman", 12))
        self.avail_label.grid(row=0, column=0, padx=5, pady=5)

        self.radio_available= tk.Radiobutton(self.avail_frame, text="Available", variable=self.avail_var, value=True)
        self.radio_available.grid(row=0, column=1, padx=5, pady=5)
        self.radio_unavailable= tk.Radiobutton(self.avail_frame, text="Unavailable", variable=self.avail_var, value=False)
        self.radio_unavailable.grid(row=0, column=2, padx=5, pady=5)

        #-------------------------------------------------------------------------------------------------------------------------

        self.rental_vehicles_list = tk.Listbox(self.main_container, selectmode=tk.SINGLE, width=120, height=20)
        self.rental_vehicles_list.bind('<<ListboxSelect>>', self.load_selected_data)
        self.rental_vehicles_list.pack(pady=10)

        self.summary_label = tk.Label(self.main_container, text="", font=("Times New Roman", 11, "bold"), fg="navy")
        self.summary_label.pack(pady=5)

        self.delete_action_btn = tk.Button(self.main_container, text="Delete Vehicle Selected", command=self.delete_rental_vehicle, bg="tomato")

        #Buttons

        self.form_frame.pack_forget()

        self.add_btn = tk.Button(self.btn_frame, text="Add Rental Vehicle", command=self.open_add_view, width=20)
        self.add_btn.grid(row=0, column=0, padx=15, pady=15)

        self.show_btn = tk.Button(self.btn_frame, text="Show Rental Vehicles", command=self.open_show_view, width=20)
        self.show_btn.grid(row=0, column=1, padx=15, pady=15)

        self.delete_btn = tk.Button(self.btn_frame, text="Delete Rental Vehicle", command=self.open_delete_view, width=20)
        self.delete_btn.grid(row=1, column=0, padx=15, pady=15)

        self.update_btn = tk.Button(self.btn_frame, text="Update Rental Vehicle", command=self.open_update_view, width=20)
        self.update_btn.grid(row=1, column=1, padx=15, pady=15)

        # -----------------------------------------------------------------



    def add_rental_vehicle(self):
        make = self.make_entry.get()
        model = self.model_entry.get()
        year=self.year_entry.get()
        fuel=self.fuel_var.get()
        avail=self.avail_var.get()
        daily_tariff=self.daily_tariff_entry.get()

        try:
            query = "INSERT INTO Vehicles (Make, Model, Year, Fuel, Available, DailyTariff) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (make, model, year, fuel, avail, daily_tariff)
            self.cursor.execute(query, values)
            self.connection.commit()

            messagebox.showinfo("Success!", "Rental Vehicle added successfully!")
            self.clear_form()
            self.show_rental_vehicles()

        except Exception as e:
            messagebox.showerror("Error", f"Error when trying to add Rental Vehicle: {str(e)}")


    def show_rental_vehicles(self):
        try:
            self.rental_vehicles_list.delete(0, tk.END)
            query = "SELECT * FROM Vehicles"
            self.cursor.execute(query)
            vehicles = self.cursor.fetchall()

            for vehicle in vehicles:
                self.rental_vehicles_list.insert(tk.END, f"ID: {vehicle[0]}, Make: {vehicle[1]}, "
                f"Model: {vehicle[2]}, Year: {vehicle[3]}, Fuel: {vehicle[4]}, Available: {vehicle[5]}, Daily Tariff: {vehicle[6]} ")

            if vehicles:
                makes_list = [vehicle[1] for vehicle in vehicles]
                make_counts = Counter(makes_list)
                summary_text = " | ".join([f"{make}: {count}" for make, count in make_counts.items()])
                self.summary_label.config(text=f"Summary by Make -> {summary_text}")
            else:
                self.summary_label.config(text="No vehicles registered in the fleet.")

        except Exception as e:
            messagebox.showerror("Error", f"Error when trying to show Rental Vehicles: {str(e)}")


    def delete_rental_vehicle(self):
        try:
            selection = self.rental_vehicles_list.curselection()

            if selection:
                selected_rental_vehicle= self.rental_vehicles_list.get(selection[0])
                id_rental_vehicle = extract_id_number(selected_rental_vehicle)

                select_query = "SELECT Make, Model, Year FROM Vehicles WHERE ID = %s"
                self.cursor.execute(select_query, (id_rental_vehicle,))
                vehicle_data = self.cursor.fetchone()

                if vehicle_data:
                    make = vehicle_data[0]
                    model = vehicle_data[1]
                    year = vehicle_data[2]

                    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the {make} {model} {year}?")

                    if confirm:
                        delete_query = "DELETE FROM Vehicles WHERE ID = %s"
                        self.cursor.execute(delete_query, (id_rental_vehicle,))
                        self.connection.commit()

                        messagebox.showinfo("Success!", f"Rental Vehicle {make} {model} {year} has been successfully deleted")
                        self.show_rental_vehicles()
                        self.clear_form()
                    else:
                        messagebox.showinfo("Cancelled", "The vehicle is safe. Deletion cancelled.")

        except Exception as e:
            messagebox.showerror("Error", f"Error when trying to delete Rental Vehicle: {str(e)}")


    def update_rental_vehicle(self):
        try:

            selection = self.rental_vehicles_list.curselection()

            if not selection:
                messagebox.showwarning("Warning", "Please select a vehicle from the list to update.")
                return

            selected_rental_vehicle = self.rental_vehicles_list.get(selection[0])
            id_rental_vehicle = extract_id_number(selected_rental_vehicle)

            make = self.make_entry.get()
            model = self.model_entry.get()
            year=self.year_entry.get()
            fuel=self.fuel_var.get()
            avail=self.avail_var.get()
            daily_tariff=self.daily_tariff_entry.get()

            query = "UPDATE Vehicles SET Make=%s, Model=%s, Year=%s, Fuel=%s, Available=%s, DailyTariff=%s WHERE ID = %s"
            values = (make, model, year, fuel, avail, daily_tariff , id_rental_vehicle)
            self.cursor.execute(query, values)
            self.connection.commit()

            messagebox.showinfo("Success", f"Rental Vehicle {make} {model} (ID: {id_rental_vehicle}) has been successfully updated")
            self.show_rental_vehicles()
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", f"Error when trying to update the Rental Vehicle {str(e)}")


    def load_selected_data(self, event):
        selection = self.rental_vehicles_list.curselection()

        if selection:
            selected_rental_vehicle = self.rental_vehicles_list.get((selection[0]))
            rental_vehicle_id = extract_id_number(selected_rental_vehicle)

            query = "SELECT * FROM Vehicles WHERE ID = %s"
            self.cursor.execute(query, (rental_vehicle_id,))
            rental_vehicle_data = self.cursor.fetchone()

            if rental_vehicle_data:

                self.make_entry.delete(0, tk.END)
                self.make_entry.insert(0, rental_vehicle_data[1])


                self.model_entry.delete(0, tk.END)
                self.model_entry.insert(0, rental_vehicle_data[2])


                self.year_entry.delete(0, tk.END)
                self.year_entry.insert(0, rental_vehicle_data[3])


                self.fuel_var.set(rental_vehicle_data[4])

                self.avail_var.set(bool(rental_vehicle_data[5]))

                self.daily_tariff_entry.delete(0, tk.END)
                self.daily_tariff_entry.insert(0, rental_vehicle_data[6])


    def clear_form(self):
        self.make_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.daily_tariff_entry.delete(0, tk.END)

        self.fuel_var.set("Gasoline")
        self.avail_var.set(True)

        self.rental_vehicles_list.selection_clear(0, tk.END)

    def hide_all_frames(self):
        self.form_frame.pack_forget()
        self.rental_vehicles_list.pack_forget()
        self.delete_action_btn.pack_forget()
        self.summary_label.config(text="")

    def open_add_view(self):
        self.hide_all_frames()
        self.clear_form()
        self.form_frame.pack(pady=8)
        self.save_btn.config(text="Save Vehicle", command=self.add_rental_vehicle, bg="lightgreen")

    def open_update_view(self):
        self.hide_all_frames()
        self.rental_vehicles_list.config(height=8)
        self.rental_vehicles_list.pack(pady=10)
        self.show_rental_vehicles()
        self.summary_label.config(text="")
        self.form_frame.pack(pady=8)
        self.save_btn.config(text="Save Changes", command=self.update_rental_vehicle, bg="lightblue")

    def open_show_view(self):
        self.hide_all_frames()
        self.rental_vehicles_list.config(height=20)
        self.rental_vehicles_list.pack(pady=10)
        self.show_rental_vehicles()

    def open_delete_view(self):
        self.hide_all_frames()
        self.rental_vehicles_list.config(height=20)
        self.rental_vehicles_list.pack(pady=10)
        self.show_rental_vehicles()
        self.delete_action_btn.pack(pady=5)

    def return_to_menu(self):
        self.hide_all_frames()
        self.clear_form()
        self.open_show_view()

if __name__ == "__main__":
    root = tk.Tk()
    app = RentalVehicleApp(root)
    root.mainloop()


    app.cursor.close()
    app.connection.close()