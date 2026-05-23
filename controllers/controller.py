import tkinter as tk
from models.model import Model


class Controller:
    def __init__(self, view):
        super().__init__()

        self.model = Model()
        self.view = view
        self.selected_hotel_id = None
        self.selected_employee_id = None
        self.selected_guest_id = None

    def refresh_hotels(self):

        for item in self.view.hotel_table.get_children():
            self.view.hotel_table.delete(item)

        self.view.map_view.delete_all_marker()

        filter_value = self.view.filter_entry.get().lower().strip()
        filter_type = self.view.filter_var.get()

        hotels = self.model.get_hotels()

        for h in hotels:

            hotel_id = h.id
            hotel_name = h.name or ""

            full_address = h.address or ""

            rooms_total = h.rooms_total or 0
            rooms_free = h.rooms_free or 0

            lat = h.lat
            lon = h.lon

            name_lower = hotel_name.lower()
            address_lower = full_address.lower()

            try:

                street, city = full_address.split(",")

                street = street.strip()
                city = city.strip()

            except ValueError:

                street = full_address
                city = ""

            match = True

            if filter_value:

                if filter_type == "Nazwa":
                    match = filter_value in name_lower

                elif filter_type == "Adres":
                    match = filter_value in address_lower

                elif filter_type == "Miasto":
                    match = filter_value in city.lower()

                elif filter_type == "Wolne pokoje":

                    try:
                        match = rooms_free >= int(filter_value)

                    except ValueError:
                        match = False

            if match:

                self.view.hotel_table.insert(
                    "",
                    tk.END,
                    values=(
                        hotel_name,
                        street,
                        city.title(),
                        f"{rooms_free}/{rooms_total}"
                    )
                )

                if lat is not None and lon is not None:
                    h.marker = self.view.map_view.set_marker(
                        lat,
                        lon,
                        text=hotel_name,
                        marker_color_circle="pink",
                        marker_color_outside="#FF00FF"
                    )

    def save_hotel_ui(self):

        name = self.view.name_entry.get()
        address = self.view.address_entry.get()

        rooms_total = self.view.rooms_total_entry.get()
        rooms_free = self.view.rooms_free_entry.get()

        if not name or not address:
            return

        try:
            rooms_total = int(rooms_total)
            rooms_free = int(rooms_free)

        except ValueError:
            return

        if self.selected_hotel_id:

            self.model.update_hotel(
                self.selected_hotel_id,
                name,
                address,
                rooms_total,
                rooms_free
            )

            self.selected_hotel_id = None

            self.view.save_button.configure(
                text="Dodaj hotel"
            )

        else:

            self.model.add_hotel(
                name,
                address,
                rooms_total,
                rooms_free
            )

        self.view.name_entry.delete(0, tk.END)
        self.view.address_entry.delete(0, tk.END)

        self.view.rooms_total_entry.delete(0, tk.END)
        self.view.rooms_free_entry.delete(0, tk.END)

        self.refresh_hotels()

        self.load_hotels_to_employee_combo()
        self.load_hotels_guests()

    def edit_hotel_ui(self):

        selected = self.view.hotel_table.selection()

        if not selected:
            return

        item = selected[0]

        index = self.view.hotel_table.index(item)

        hotel = self.model.get_hotels()[index]

        self.selected_hotel_id = hotel.id

        self.view.name_entry.delete(0, tk.END)
        self.view.address_entry.delete(0, tk.END)

        self.view.rooms_total_entry.delete(0, tk.END)
        self.view.rooms_free_entry.delete(0, tk.END)

        self.view.name_entry.insert(0, hotel.name)
        self.view.address_entry.insert(0, hotel.address)

        self.view.rooms_total_entry.insert(0, hotel.rooms_total)
        self.view.rooms_free_entry.insert(0, hotel.rooms_free)

        self.view.save_button.configure(
            text="Zapisz zmiany"
        )

    def delete_hotel_ui(self):

        selected = self.view.hotel_table.selection()

        if not selected:
            return

        item = selected[0]

        index = self.view.hotel_table.index(item)

        hotel = self.model.get_hotels()[index]

        self.model.delete_hotel(hotel.id)

        self.refresh_hotels()

    def load_hotels_to_employee_combo(self):
        self.view.employee_hotel_combo["values"] = [
            f"{h.id} - {h.name}" for h in self.model.get_hotels()
        ]

    def add_employee_ui(self):

        name = self.view.employee_name_entry.get()
        position = self.view.employee_position_entry.get()
        contract = self.view.employee_contract_entry.get()
        date = self.view.employee_date_entry.get()
        address = self.view.employee_address_entry.get()
        hotel = self.view.employee_hotel_var.get()

        if not name or not hotel:
            return

        hotel_id = int(hotel.split(" - ")[0])

        if self.selected_employee_id:

            self.model.update_employee(
                self.selected_employee_id,
                name,
                position,
                contract,
                date,
                hotel_id,
                address
            )

            self.selected_employee_id = None
            self.view.add_employee_button.configure(
                text="Dodaj pracownika"
            )

        else:

            self.model.add_employee(
                name,
                position,
                contract,
                date,
                hotel_id,
                address
            )

        self.view.employee_name_entry.delete(0, tk.END)
        self.view.employee_position_entry.delete(0, tk.END)
        self.view.employee_contract_entry.delete(0, tk.END)
        self.view.employee_date_entry.delete(0, tk.END)
        self.view.employee_address_entry.delete(0, tk.END)

        self.refresh_employees()

    def refresh_employees(self):

        for item in self.view.employee_tree.get_children():
            self.view.employee_tree.delete(item)
            self.view.employee_map.delete_all_marker()

        for h in self.model.get_hotels():

            hotel_name = h.name

            hotel_item = self.view.employee_tree.insert(
                "",
                tk.END,
                text=hotel_name
            )

            employees = self.model.get_employees_by_hotel(h.id)

            for e in employees:
                employee_name = e.name
                position = e.position

                self.view.employee_tree.insert(
                    hotel_item,
                    tk.END,
                    text=employee_name,
                    values=(e.id, position)
                )

                if e.lat is not None and e.lon is not None:
                    e.marker = self.view.employee_map.set_marker(
                        e.lat,
                        e.lon,
                        text=f"{employee_name}\n{position}",
                        marker_color_circle="pink",
                        marker_color_outside="#FF00FF"
                    )

    def edit_employee_ui(self):

        selected = self.view.employee_tree.selection()

        if not selected:
            return

        item = selected[0]

        employee_id = self.view.employee_tree.item(item)["values"][0]

        employees = []

        for h in self.model.get_hotels():
            employees.extend(
                self.model.get_employees_by_hotel(h.id)
            )

        employee = next(
            e for e in employees if e.id == employee_id
        )

        self.selected_employee_id = employee.id

        self.view.employee_name_entry.delete(0, tk.END)
        self.view.employee_position_entry.delete(0, tk.END)
        self.view.employee_contract_entry.delete(0, tk.END)
        self.view.employee_date_entry.delete(0, tk.END)
        self.view.employee_address_entry.delete(0, tk.END)

        self.view.employee_name_entry.insert(0, employee.name)
        self.view.employee_position_entry.insert(0, employee.position)
        self.view.employee_contract_entry.insert(0, employee.contract)
        self.view.employee_date_entry.insert(0, employee.date)

        self.view.add_employee_button.configure(
            text="Zapisz zmiany"
        )

    def delete_employee_ui(self):

        selected = self.view.employee_tree.selection()

        if not selected:
            return

        item = selected[0]

        employee_id = self.view.employee_tree.item(item)["values"][0]

        self.model.delete_employee(employee_id)

        self.refresh_employees()

    def load_hotels_guests(self):
        self.view.guest_hotel_combo["values"] = [
            f"{h.id} - {h.name}" for h in self.model.get_hotels()
        ]

    def add_guest_ui(self):

        name = self.view.guest_name_entry.get()
        phone = self.view.phone_entry.get()
        email = self.view.email_entry.get()
        id_type = self.view.id_type_var.get()
        id_number = self.view.id_number_entry.get()
        hotel = self.view.guest_hotel_var.get()

        if not name or not hotel:
            return

        hotel_id = int(hotel.split(" - ")[0])

        if self.selected_guest_id:

            self.model.update_guest(
                self.selected_guest_id,
                name,
                phone,
                email,
                id_type,
                id_number,
                hotel_id
            )

            self.selected_guest_id = None

            self.view.guest_tree.selection_remove(
                self.view.guest_tree.selection()
            )

            self.view.add_guest_button.configure(
                text="Dodaj gościa"
            )

        else:

            self.model.add_guest(
                name,
                phone,
                email,
                id_type,
                id_number,
                hotel_id
            )

        self.view.guest_name_entry.delete(0, tk.END)
        self.view.phone_entry.delete(0, tk.END)
        self.view.email_entry.delete(0, tk.END)
        self.view.id_number_entry.delete(0, tk.END)

        self.view.guest_hotel_var.set("")
        self.view.id_type_combo.current(0)

        self.refresh_guests()

    def refresh_guests(self):

        for item in self.view.guest_tree.get_children():
            self.view.guest_tree.delete(item)
            self.view.guest_map.delete_all_marker()

        for h in self.model.get_hotels():

            hotel_name = h.name

            hotel_item = self.view.guest_tree.insert(
                "",
                tk.END,
                text=hotel_name
            )

            guests = self.model.get_guests_by_hotel(h.id)

            for g in guests:
                guest_name = g.name

                self.view.guest_tree.insert(
                    hotel_item,
                    tk.END,
                    text=guest_name,
                    values=(g.id,)
                )

                if g.lat is not None and g.lon is not None:
                    g.marker = self.view.guest_map.set_marker(
                        g.lat,
                        g.lon,
                        text=f"{guest_name}\n{hotel_name}",
                        marker_color_circle="pink",
                        marker_color_outside="#FF00FF"
                    )

    def edit_guest_ui(self):

        selected = self.view.guest_tree.selection()

        if not selected:
            return

        item = selected[0]

        values = self.view.guest_tree.item(item)["values"]

        if not values:
            return

        guest_id = int(values[0])

        guests = []

        for h in self.model.get_hotels():
            guests.extend(
                self.model.get_guests_by_hotel(h.id)
            )

        guest = next(
            g for g in guests if int(g.id) == int(guest_id)
        )

        self.selected_guest_id = guest.id

        self.view.guest_name_entry.delete(0, tk.END)
        self.view.phone_entry.delete(0, tk.END)
        self.view.email_entry.delete(0, tk.END)
        self.view.id_number_entry.delete(0, tk.END)

        self.view.guest_name_entry.insert(0, guest.name)
        self.view.phone_entry.insert(0, guest.phone)
        self.view.email_entry.insert(0, guest.email)
        self.view.id_type_var.set(guest.id_type)
        self.view.id_number_entry.insert(0, guest.id_number)

        for h in self.model.get_hotels():

            if h.id == guest.hotel_id:
                self.view.guest_hotel_var.set(
                    f"{h.id} - {h.name}"
                )

        self.view.add_guest_button.configure(
            text="Zapisz zmiany"
        )

    def delete_guest_ui(self):

        selected = self.view.guest_tree.selection()

        if not selected:
            return

        item = selected[0]

        values = self.view.guest_tree.item(item)["values"]

        if not values:
            return

        guest_id = int(values[0])

        self.model.delete_guest(guest_id)

        self.refresh_guests()
