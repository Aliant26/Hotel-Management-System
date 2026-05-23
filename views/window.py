import tkinter as tk
from tkinter import ttk
from customtkinter import *
from tkintermapview import TkinterMapView
from controllers.controller import Controller


class Window(CTk):

    def __init__(self):
        super().__init__()

        self.title("Hotel Management System")
        self.geometry("1200x800")
        self.configure(bg="#f5f5f5")

        set_appearance_mode("light")

        self.controller = Controller(self)
        self.create_widgets()

        self.controller.refresh_hotels()
        self.controller.refresh_employees()
        self.controller.refresh_guests()

        self.controller.load_hotels_to_employee_combo()
        self.controller.load_hotels_guests()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_hotels = CTkFrame(self.notebook)
        self.tab_employees = CTkFrame(self.notebook)
        self.tab_guests = CTkFrame(self.notebook)

        self.notebook.add(self.tab_hotels, text="Hotele")
        self.notebook.add(self.tab_employees, text="Pracownicy")
        self.notebook.add(self.tab_guests, text="Goście")

        self.hotel_frame = CTkFrame(self.tab_hotels, corner_radius=15)

        self.hotel_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.hotel_frame.grid_rowconfigure(0, weight=1)
        self.hotel_frame.grid_columnconfigure(0, weight=1)
        self.hotel_frame.grid_columnconfigure(1, weight=2)
        self.hotel_frame.grid_columnconfigure(2, weight=2)

        self.form_frame = CTkFrame(self.hotel_frame, corner_radius=15)
        self.form_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        CTkLabel( self.form_frame,text="Formularz:").pack(anchor="w", padx=10, pady=5)

        CTkLabel(self.form_frame, text="Nazwa hotelu").pack(anchor="w", pady=(10, 2))
        self.name_entry = CTkEntry(self.form_frame, width=250)
        self.name_entry.pack(pady=10)

        CTkLabel(self.form_frame, text="Adres \n (Format: ulica numer, miejscowość)").pack(anchor="w", pady=(10, 2))
        self.address_entry = CTkEntry(self.form_frame, width=250)
        self.address_entry.pack(pady=10)

        CTkLabel(self.form_frame, text="Liczba pokoi").pack(anchor="w")
        self.rooms_total_entry = CTkEntry(self.form_frame, width=250)
        self.rooms_total_entry.pack(pady=5)

        CTkLabel(self.form_frame, text="Wolne pokoje").pack(anchor="w")
        self.rooms_free_entry = CTkEntry(self.form_frame, width=250)
        self.rooms_free_entry.pack(pady=5)

        self.list_frame = CTkFrame(self.hotel_frame, corner_radius=15, fg_color="transparent")
        self.list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        CTkLabel(self.list_frame, text="Lista hoteli").pack(anchor="w", padx=10, pady=5)

        self.filter_frame = CTkFrame(self.list_frame, fg_color="transparent")
        self.filter_frame.pack(fill="x", padx=10, pady=5)

        self.filter_var = tk.StringVar()
        self.filter_data = ttk.Combobox(
            self.filter_frame,
            textvariable=self.filter_var,
            state="readonly",
            width=15
        )

        self.filter_data["values"] = [
            "Nazwa",
            "Miasto",
            "Wolne pokoje"
        ]

        self.filter_data.current(0)
        self.filter_data.pack(side="left", padx=5)

        self.filter_entry = CTkEntry(self.filter_frame, placeholder_text="Wpisz wartość...")
        self.filter_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.filter_entry.bind(
            "<KeyRelease>",
            lambda event: self.controller.refresh_hotels()
        )

        self.filter_data.bind(
            "<<ComboboxSelected>>",
            lambda event: self.controller.refresh_hotels()
        )

        self.hotel_table = ttk.Treeview(
            self.list_frame,
            columns=("hotel", "address", "city", "rooms"),
            show="headings",
            height=20
        )

        self.hotel_table.heading("hotel", text="Hotel")
        self.hotel_table.heading("address", text="Ulica")
        self.hotel_table.heading("city", text="Miasto")
        self.hotel_table.heading("rooms", text="Pokoje")

        self.hotel_table.column("hotel", width=180)
        self.hotel_table.column("address", width=180)
        self.hotel_table.column("city", width=120)
        self.hotel_table.column("rooms", width=120)

        self.hotel_table.pack(fill="both", expand=True, padx=5, pady=5)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.hotel_table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.hotel_table.yview)

        self.map_frame = CTkFrame(self.hotel_frame, corner_radius=15, fg_color="transparent")
        self.map_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        self.map_frame.grid_rowconfigure(1, weight=1)
        self.map_frame.grid_columnconfigure(0, weight=1)

        self.map_label = CTkLabel(self.map_frame, text="Mapa hoteli")

        self.map_view = TkinterMapView(
            self.map_frame,
            width=400,
            height=500
        )

        self.map_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.map_view.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.map_view.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

        self.map_view.set_position(52.2297, 21.0122)
        self.map_view.set_zoom(6)

        self.button_frame = CTkFrame(self.tab_hotels)
        self.button_frame.pack(pady=10)

        self.save_button = CTkButton(self.button_frame, text="Dodaj hotel", corner_radius=30,
                                     fg_color="#C850C0", hover_color="#4158D0", command=self.controller.save_hotel_ui)
        self.save_button.pack(side="left", padx=5)

        self.edit_button = CTkButton(self.button_frame, text="Edytuj hotel", corner_radius=30,
                                     fg_color="#C850C0", hover_color="#4158D0", command=self.controller.edit_hotel_ui)
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = CTkButton(self.button_frame, text="Usuń hotel", corner_radius=30,
                                       fg_color="#C850C0", hover_color="#4158D0",
                                       command=self.controller.delete_hotel_ui)
        self.delete_button.pack(side="left", padx=5)

        self.employee_frame = CTkFrame(self.tab_employees, corner_radius=15, fg_color="transparent")
        self.employee_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_emp_frame = CTkFrame(self.employee_frame, corner_radius=15, fg_color="transparent")
        self.left_emp_frame.pack(side="left", fill="y", padx=10)

        CTkLabel(self.left_emp_frame,text="Formularz:").grid(row=0, column=0, columnspan=2, sticky="w", pady=(5, 15))

        CTkLabel(self.left_emp_frame, text="Imię i nazwisko").grid(row=1, column=0, padx=5, pady=5)
        self.employee_name_entry = CTkEntry(self.left_emp_frame, width=200)
        self.employee_name_entry.grid(row=1, column=1)

        CTkLabel(self.left_emp_frame, text="Adres").grid(row=2, column=0, padx=5, pady=5)
        self.employee_address_entry = CTkEntry(self.left_emp_frame, width=200)
        self.employee_address_entry.grid(row=2, column=1)

        CTkLabel(self.left_emp_frame, text="Stanowisko").grid(row=4, column=0, padx=5, pady=5)
        self.employee_position_entry = CTkEntry(self.left_emp_frame, width=200)
        self.employee_position_entry.grid(row=4, column=1)

        CTkLabel(self.left_emp_frame, text="Rodzaj umowy").grid(row=5, column=0, padx=5, pady=5)
        self.employee_contract_entry = CTkEntry(self.left_emp_frame, width=200)
        self.employee_contract_entry.grid(row=5, column=1)

        CTkLabel(self.left_emp_frame, text="Data zakończenia umowy").grid(row=6, column=0, padx=5, pady=5)
        self.employee_date_entry = CTkEntry(self.left_emp_frame, width=200)
        self.employee_date_entry.grid(row=6, column=1)

        CTkLabel(self.left_emp_frame, text="Hotel").grid(row=3, column=0, padx=5, pady=5)
        self.employee_hotel_var = tk.StringVar()

        self.employee_hotel_combo = ttk.Combobox(
            self.left_emp_frame,
            textvariable=self.employee_hotel_var,
            state="readonly",
            width=35
        )
        self.employee_hotel_combo.grid(row=3, column=1)

        self.emp_list_frame = CTkFrame(self.employee_frame, corner_radius=15, fg_color="transparent")
        self.emp_list_frame.pack(side="left", fill="both", expand=True)

        CTkLabel(self.emp_list_frame, text="Lista pracowników").pack(anchor="w", padx=10, pady=5)

        self.emp_map_frame = CTkFrame(
            self.employee_frame,
            corner_radius=15,
            fg_color="transparent"
        )

        self.emp_map_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.employee_map_label = CTkLabel(
            self.emp_map_frame,
            text="Mapa pracowników"
        )

        self.employee_map_label.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        self.employee_map = TkinterMapView(
            self.emp_map_frame,
            width=300,
            height=450
        )

        self.employee_map.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.employee_map.set_tile_server(
            "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
        )

        self.employee_map.set_position(52.2297, 21.0122)
        self.employee_map.set_zoom(6)

        self.employee_tree = ttk.Treeview(
            self.emp_list_frame,
            columns=("id", "position")
        )

        self.employee_tree.heading("#0", text="Pracownik")
        self.employee_tree.heading("position", text="Stanowisko")

        self.employee_tree.column("id", width=0, stretch=False)
        self.employee_tree.column("position", width=150)

        self.employee_tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.employee_button_frame = CTkFrame(self.tab_employees, fg_color="transparent")
        self.employee_button_frame.pack(pady=10)

        self.add_employee_button = CTkButton(self.employee_button_frame, text="Dodaj pracownika", corner_radius=30,
                                             fg_color="#C850C0", hover_color="#4158D0",
                                             command=self.controller.add_employee_ui)
        self.add_employee_button.pack(side="left", padx=5)

        self.edit_employee_button = CTkButton(self.employee_button_frame, text="Aktualizuj dane", corner_radius=30,
                                              fg_color="#C850C0", hover_color="#4158D0",
                                              command=self.controller.edit_employee_ui)
        self.edit_employee_button.pack(side="left", padx=5)

        self.delete_employee_button = CTkButton(self.employee_button_frame, text="Usuń pracownika", corner_radius=30,
                                                fg_color="#C850C0", hover_color="#4158D0",
                                                command=self.controller.delete_employee_ui)
        self.delete_employee_button.pack(side="left", padx=5)

        self.guest_frame = CTkFrame(self.tab_guests, corner_radius=15, fg_color="transparent")
        self.guest_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_guest_frame = CTkFrame(self.guest_frame, corner_radius=15, fg_color="transparent")
        self.left_guest_frame.pack(side="left", fill="y", padx=10)

        CTkLabel(self.left_guest_frame, text="Formularz:").grid(row=0, column=0, columnspan=2, sticky="w", pady=(5, 15))

        CTkLabel(self.left_guest_frame, text="Imię i nazwisko").grid(row=1, column=0, padx=5, pady=5)
        self.guest_name_entry = CTkEntry(self.left_guest_frame, width=200)
        self.guest_name_entry.grid(row=1, column=1)

        CTkLabel(self.left_guest_frame, text="Telefon").grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = CTkEntry(self.left_guest_frame, width=200)
        self.phone_entry.grid(row=2, column=1)

        CTkLabel(self.left_guest_frame, text="Email").grid(row=3, column=0, padx=5, pady=5)
        self.email_entry = CTkEntry(self.left_guest_frame, width=200)
        self.email_entry.grid(row=3, column=1)

        CTkLabel(self.left_guest_frame, text="Typ ID").grid(row=4, column=0, padx=5, pady=5)
        self.id_type_var = tk.StringVar()

        self.id_type_combo = ttk.Combobox(
            self.left_guest_frame,
            textvariable=self.id_type_var,
            state="readonly",
            width=25
        )
        self.id_type_combo["values"] = ["Dowód", "Paszport", "Prawo jazdy", "Legitymacja"]
        self.id_type_combo.current(0)
        self.id_type_combo.grid(row=4, column=1)

        CTkLabel(self.left_guest_frame, text="Numer ID").grid(row=5, column=0, padx=5, pady=5)
        self.id_number_entry = CTkEntry(self.left_guest_frame, width=200)
        self.id_number_entry.grid(row=5, column=1)

        CTkLabel(self.left_guest_frame, text="Hotel").grid(row=6, column=0, padx=5, pady=5)
        self.guest_hotel_var = tk.StringVar()

        self.guest_hotel_combo = ttk.Combobox(
            self.left_guest_frame,
            textvariable=self.guest_hotel_var,
            state="readonly",
            width=25
        )
        self.guest_hotel_combo.grid(row=6, column=1)

        self.guest_list_frame = CTkFrame(self.guest_frame)
        self.guest_list_frame.pack(side="left", fill="both", expand=True)

        CTkLabel(self.guest_list_frame, text="Lista gości").pack(anchor="w", padx=10, pady=5)

        self.guest_map_frame = CTkFrame(
            self.guest_frame,
            corner_radius=15,
            fg_color="transparent"
        )

        self.guest_map_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.guest_map_label = CTkLabel(
            self.guest_map_frame,
            text="Mapa gości"
        )

        self.guest_map_label.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        self.guest_map = TkinterMapView(
            self.guest_map_frame,
            width=300,
            height = 450
        )

        self.guest_map.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.guest_map.set_tile_server(
            "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
        )

        self.guest_map.set_position(52.2297, 21.0122)
        self.guest_map.set_zoom(6)

        self.guest_tree = ttk.Treeview(
            self.guest_list_frame,
            columns=("id",)
        )

        self.guest_tree.heading("#0", text="Goście")
        self.guest_tree.column("id", width=0, stretch=False)

        self.guest_tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.guest_button_frame = CTkFrame(
            self.tab_guests,
            fg_color="transparent"
        )

        self.guest_button_frame.pack(pady=10)

        self.add_guest_button = CTkButton(self.guest_button_frame, text="Dodaj gościa", corner_radius=30,
                                          fg_color="#C850C0", hover_color="#4158D0",
                                          command=self.controller.add_guest_ui
                                          )

        self.add_guest_button.pack(side="left", padx=5)

        self.edit_guest_button = CTkButton(self.guest_button_frame, text="Aktualizuj dane", corner_radius=30,
                                           fg_color="#C850C0", hover_color="#4158D0",
                                           command=self.controller.edit_guest_ui
                                           )

        self.edit_guest_button.pack(side="left", padx=5)

        self.delete_guest_button = CTkButton(self.guest_button_frame, text="Usuń gościa", corner_radius=30,
                                             fg_color="#C850C0", hover_color="#4158D0",
                                             command=self.controller.delete_guest_ui
                                             )

        self.delete_guest_button.pack(side="left", padx=5)
