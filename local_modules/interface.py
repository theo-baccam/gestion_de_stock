from tkinter import *
from tkinter import ttk

from .database import Database as db


class Interface():
    def __init__(self):
        self.connected = False
        self.password = None
        self.selected_id = None

        self.root = Tk()
        self.root.title("Téeo's Stock Manager")
        self.root.resizable(False, False)
        self.render_password_area()
        self.root.mainloop()

        if self.connected:
            self.root = Tk()
            self.root.title("Théo's Stock Manager")
            self.render_main_frame()
            self.root.mainloop()

    def refresh_main_frame(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.render_main_frame()

    def render_password_area(self):
        password_frame = ttk.Frame(self.root)

        password_text = ttk.Label(password_frame, text="Mot de passe du serveur:")
        password_text.pack(padx=8, pady=8, side=LEFT)

        password_field = ttk.Entry(password_frame, show="*")
        password_field.pack(padx=8, pady=8, side = LEFT)

        def attempt_connection():
            password = password_field.get()
            self.connected = db(password).check_connection()
            if self.connected:
                self.password = password
                self.root.destroy()
            else:
                self.password = None

        password_button = ttk.Button(
            password_frame,
            text="Se connecter",
            command=attempt_connection
        )
        password_button.pack(padx=4, pady=4, side = LEFT)

        password_frame.pack(padx=8, pady=8, side=LEFT)

    def render_main_frame(self):
        main_frame = ttk.Frame(self.root)
        self.render_list_frame(main_frame)
        self.render_remove_button(main_frame)
        self.render_add_button(main_frame)
        self.render_refresh_button(main_frame)
        main_frame.pack(padx=16, pady=16, side=BOTTOM)

    def render_list_frame(self, main_frame):
        list_frame = ttk.Frame(main_frame)
        self.render_product_list(list_frame)
        list_frame.pack(padx=8, pady=8, side=LEFT, fill=BOTH, expand=True)

    def render_product_list(self, list_frame):
        def get_selection_id(event):
            try:
                item = product_list.selection()[0]
                selected_id = product_list.item(item, "values")[0]
                self.selected_id = selected_id
            except:
                self.selected_id = None

        def select_attribute(event):
            column = product_list.identify_column(event.x)
            attribute = product_list.heading(column)["text"]
            if attribute == "":
                attribute = "name"
            windows = {
                "name": self.update_name_window,
                "description": self.update_description_window,
                "price": self.update_price_window,
                "quantity": self.update_quantity_window,
                "category": self.update_category_window
            }
            if attribute in windows:
                windows[attribute]()
            
        columns = ("id", "name", "description", "price", "quantity", "category")
        product_list = ttk.Treeview(
            list_frame,
            columns=columns
        )

        product_list.column("#0", width=0, stretch=NO)
        for column in columns:
            product_list.heading(column, text=column)
        product_list.column("id", width=16*3)
        product_list.column("name", width=16*8)
        product_list.column("description", width=16*16)
        product_list.column("price", width=16*4)
        product_list.column("quantity", width=16*4)
        product_list.column("category", width=16*8)

        for product in db(self.password).get_products():
            product_list.insert(
                "",
                END,
                values=(
                    product["id"],
                    product["name"],
                    product["description"],
                    f"{product["price"]} G",
                    product["quantity"],
                    db(self.password).get_category_name(product["id_category"])
                )
            )

        product_list.bind("<ButtonRelease-1>", get_selection_id)
        product_list.bind("<Double-Button-1>", select_attribute)

        scrollbar = ttk.Scrollbar(
            list_frame,
            orient=VERTICAL,
            command=product_list.yview
        )
        scrollbar.pack(side=RIGHT, fill=Y)

        product_list.config(yscrollcommand=scrollbar.set)
        product_list.pack(padx=4, pady=4, side=TOP)

    def render_refresh_button(self, main_frame):
        def refresh(event):
            self.refresh_main_frame()

        refresh_button = ttk.Button(main_frame, text = "Rafraichir")
        refresh_button.pack(padx=8, pady=8, side=TOP)
        refresh_button.bind("<ButtonRelease-1>", refresh)

    def render_add_button(self, main_frame):
        def add_new_product(event):
            db(self.password).create_new_product()
            self.refresh_main_frame()

        add_button = ttk.Button(main_frame, text = "Ajouter produit")
        add_button.pack(padx=8, pady=8, side=BOTTOM)
        add_button.bind("<ButtonRelease-1>", add_new_product)

    def render_remove_button(self, main_frame):
        def remove_product(event):
            db(self.password).delete_product(self.selected_id)
            self.refresh_main_frame()

        add_button = ttk.Button(main_frame, text = "Supprimer produit")
        add_button.pack(padx=8, pady=8, side=BOTTOM)
        add_button.bind("<ButtonRelease-1>", remove_product)

    def update_name_window(self):
        def update(event):
            new_value = name_text_field.get()
            if len(new_value) <= 0 or len(new_value) > 255:
                return
            db(self.password).update_attribute_value(self.selected_id, "name", new_value)
            self.refresh_main_frame()

        update_name = Toplevel(self.root)
        update_name.grab_set()
        frame = Frame(update_name)
        name_label = ttk.Label(update_name, text="Nom:")
        name_label.pack(padx=4, pady=4, side=LEFT)

        name_text_field = ttk.Entry(update_name)
        name_text_field.pack(padx=4, pady=4, side = LEFT)
        default_text = db(self.password).get_attribute_value("name", self.selected_id)
        name_text_field.insert(0, default_text)

        name_apply_button = ttk.Button(
            update_name,
            text="Apply",
        )
        name_apply_button.pack(padx=4, pady=4, side = LEFT)
        name_apply_button.bind("<ButtonRelease-1>", update)
        frame.pack(padx=8, pady=8)

    def update_description_window(self):
        def update(event):
            new_value = description_text_field.get("1.0", "end-1c")
            if len(new_value) <= 0 or len(new_value) > 255:
                return
            db(self.password).update_attribute_value(self.selected_id, "description", new_value)
            self.refresh_main_frame()

        update_description = Toplevel(self.root)
        update_description.grab_set()
        frame = Frame(update_description)
        description_label = ttk.Label(update_description, text="Description:")
        description_label.pack(padx=4, pady=4, side=LEFT)

        description_text_field = Text(update_description, width=24, height=4, wrap=WORD)
        description_text_field.pack(padx=4, pady=4, side = LEFT)
        default_text = db(self.password).get_attribute_value("description", self.selected_id)
        description_text_field.insert("1.0", default_text)

        description_apply_button = ttk.Button(
            update_description,
            text="Apply",
        )
        description_apply_button.pack(padx=4, pady=4, side = LEFT)
        description_apply_button.bind("<ButtonRelease-1>", update)
        frame.pack(padx=8, pady=8)

    def update_price_window(self):
        def update(event):
            try:
                new_value = float(price_text_field.get())
                if new_value < 0:
                    return
                db(self.password).update_attribute_value(self.selected_id, "price", new_value)
                self.refresh_main_frame()
            except:
                return

        update_price = Toplevel(self.root)
        update_price.grab_set()
        frame = Frame(update_price)
        price_label = ttk.Label(update_price, text="Prix:")
        price_label.pack(padx=4, pady=4, side=LEFT)

        price_text_field = ttk.Entry(update_price)
        price_text_field.pack(padx=4, pady=4, side = LEFT)
        default_text = db(self.password).get_attribute_value("price", self.selected_id)
        price_text_field.insert(0, default_text)

        price_apply_button = ttk.Button(
            update_price,
            text="Apply",
        )
        price_apply_button.pack(padx=4, pady=4, side = LEFT)
        price_apply_button.bind("<ButtonRelease-1>", update)
        frame.pack(padx=8, pady=8)

    def update_quantity_window(self):
        def update(event):
            try:
                new_value = int(quantity_text_field.get())
                if new_value < 0:
                    return
                db(self.password).update_attribute_value(self.selected_id, "quantity", new_value)
                self.refresh_main_frame()
            except:
                return

        update_quantity = Toplevel(self.root)
        update_quantity.grab_set()
        frame = Frame(update_quantity)
        quantity_label = ttk.Label(update_quantity, text="Quantité:")
        quantity_label.pack(padx=4, pady=4, side=LEFT)

        quantity_text_field = ttk.Entry(update_quantity)
        quantity_text_field.pack(padx=4, pady=4, side = LEFT)
        default_text = db(self.password).get_attribute_value("quantity", self.selected_id)
        quantity_text_field.insert(0, default_text)

        quantity_apply_button = ttk.Button(
            update_quantity,
            text="Apply",
        )
        quantity_apply_button.pack(padx=4, pady=4, side = LEFT)
        quantity_apply_button.bind("<ButtonRelease-1>", update)
        frame.pack(padx=8, pady=8)

    def update_category_window(self):
        def update(event):
            selected_category = category_combobox.get()
            if len(selected_category) == 0:
                return
            id_category = selected_category[0]
            db(self.password).update_attribute_value(
                self.selected_id,
                "id_category",
                id_category
            )
            self.refresh_main_frame()

        update_category = Toplevel(self.root)
        update_category.grab_set()
        frame = Frame(update_category)
        category_label = ttk.Label(update_category, text="Catégorie:")
        category_label.pack(padx=4, pady=4, side=LEFT)

        category_combobox= ttk.Combobox(
            update_category,
            values=db(self.password).get_categories()
        )
        category_combobox.pack(padx=4, pady=4, side = LEFT)

        category_apply_button = ttk.Button(
            update_category,
            text="Apply",
        )
        category_apply_button.pack(padx=4, pady=4, side = LEFT)
        category_apply_button.bind("<ButtonRelease-1>", update)
        frame.pack(padx=8, pady=8)