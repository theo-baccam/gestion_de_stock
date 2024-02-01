from tkinter import *
from tkinter import ttk

from database import Database


class Interface():
    def __init__(self):
        self.connected = False
        self.password = None

        self.root = Tk()
        self.root.resizable(False, False)
        self.render_top_frame()
        self.root.mainloop()

        if self.connected:
            self.root = Tk()
            self.root.title("Stock Manager")
            self.root.resizable(False, False)
            self.render_main_frame()
            self.root.mainloop()

    def render_top_frame(self):
        top_frame = ttk.Frame(self.root)
        self.render_password_area(top_frame)
        top_frame.pack(padx=16, pady=16, side=TOP, fill=BOTH)

    def render_password_area(self, top_frame):
        password_frame = ttk.Frame(top_frame)

        password_text = ttk.Label(password_frame, text="Enter server password")
        password_text.pack(padx=4, pady=4, side=LEFT)

        password_field = ttk.Entry(password_frame, show="*")
        password_field.pack(padx=4, pady=4, side = LEFT)

        def attempt_connection():
            password = password_field.get()
            self.connected = Database(password).check_connection()
            if self.connected:
                self.password = password
                self.root.destroy()
            else:
                self.password = None

        password_button = ttk.Button(
            password_frame,
            text="Connect",
            command=attempt_connection
        )
        password_button.pack(padx=4, pady=4, side = LEFT)

        password_frame.pack(padx=8, pady=8, side=LEFT)

    def render_main_frame(self):
        main_frame = ttk.Frame(self.root)
        self.render_list_frame(main_frame)
        self.render_product_frame(main_frame)
        main_frame.pack(padx=16, pady=16, side=BOTTOM)

    def render_list_frame(self, main_frame):
        list_frame = ttk.Frame(main_frame)
        self.render_category_dropdown(list_frame)
        self.render_product_list(list_frame)
        list_frame.pack(padx=8, pady=8, side=LEFT)

    def render_category_dropdown(self, list_frame):
        categories = [
            "All",
            *[category for category in Database(self.password).get_categories()]
        ]

        category_dropdown = ttk.Combobox( list_frame, values=categories)
        category_dropdown.set(categories[0])
        category_dropdown.pack(padx=4, pady=4, side=TOP)

    def render_product_list(self, list_frame):
        columns = ("id", "name", "price", "quantity", "category")
        product_list = ttk.Treeview(
            list_frame,
            columns=columns
        )

        product_list.column("#0", width=0, stretch=NO)
        for column in columns:
            product_list.column(column, width=16*len(column))
            product_list.heading(column, text=column)

        for product in Database(self.password).get_products():
            product_list.insert(
                "",
                END,
                values=(
                    product["id"],
                    product["name"],
                    product["price"],
                    product["quantity"],
                    product["id_category"]
                )
            )

        scrollbar = ttk.Scrollbar(
            list_frame,
            orient=VERTICAL,
            command=product_list.yview
        )
        scrollbar.pack(side=RIGHT, fill=Y)

        product_list.config(yscrollcommand=scrollbar.set)
        product_list.pack(padx=4, pady=4, side=TOP)

    def render_product_frame(self, main_frame):
        product_frame = ttk.Frame(main_frame)
        self.render_name_frame(product_frame)
        self.render_description_frame(product_frame)
        self.render_price_frame(product_frame)
        self.render_quantity_frame(product_frame)
        self.render_category_frame(product_frame)
        self.apply_change_button(product_frame)
        product_frame.pack(padx=8, pady=8, side=RIGHT)

    def render_name_frame(self, product_frame):
        name_frame = ttk.Frame(product_frame)

        name_label = ttk.Label(name_frame, text="Name:")
        name_label.pack(padx=2, pady=2, side=LEFT)

        name_entry = ttk.Entry(name_frame)
        name_entry.pack(padx=2, pady=2, side=LEFT)

        name_frame.pack(padx=4, pady=4, side=TOP)

    def render_description_frame(self, product_frame):
        description_frame = ttk.Frame(product_frame)

        description_label = ttk.Label(description_frame, text="Description:")
        description_label.pack(padx=2, pady=2, side=LEFT)

        description_entry = Text(description_frame, height=4, width=16)
        description_entry.pack(padx=2, pady=2, side=LEFT)

        description_frame.pack(padx=4, pady=4, side=TOP)

    def render_price_frame(self, product_frame):
        price_frame = ttk.Frame(product_frame)

        price_label = ttk.Label(price_frame, text="Price:")
        price_label.pack(padx=2, pady=2, side=LEFT)

        price_entry = ttk.Entry(price_frame)
        price_entry.pack(padx=2, pady=2, side=LEFT)

        price_frame.pack(padx=4, pady=4, side=TOP)

    def render_quantity_frame(self, product_frame):
        quantity_frame = ttk.Frame(product_frame)

        quantity_label = ttk.Label(quantity_frame, text="Quantity:")
        quantity_label.pack(padx=2, pady=2, side=LEFT)

        quantity_entry = ttk.Entry(quantity_frame)
        quantity_entry.pack(padx=2, pady=2, side=LEFT)

        quantity_frame.pack(padx=4, pady=4, side=TOP)

    def render_category_frame(self, product_frame):
        category_frame = ttk.Frame(product_frame)

        category_label = ttk.Label(category_frame, text="category:")
        category_label.pack(padx=2, pady=2, side=LEFT)


        categories = [
            "All",
            *[category for category in Database(self.password).get_categories()]
        ]

        category_dropdown = ttk.Combobox(category_frame, values=categories)
        category_dropdown.set(categories[0])
        category_dropdown.pack(padx=4, pady=4, side=TOP)

        category_frame.pack(padx=4, pady=4, side=TOP)

    def apply_change_button(self, product_frame):
        apply_change = ttk.Button(product_frame, text="Apply changes")
        apply_change.pack(padx=4, pady=4, side=BOTTOM)



if __name__ == "__main__":
    Interface()