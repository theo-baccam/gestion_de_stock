import mysql.connector


class Database():
    def __init__(self, password):
        if not isinstance(password, str):
            raise ValueError("Le mot de passe doit être un string")

        self.password = password

    def connect(self):
        store = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = self.password,
            database = "store"
        )
        return store

    def check_connection(self):
        try:
            store = self.connect()
            store.close()
            return True
        except:
            return False

    def get_categories(self):
        store = self.connect()

        cursor = store.cursor()
        cursor.execute("SELECT * FROM category")
        sql_output = cursor.fetchall()
        cursor.close()
        store.close()

        category_names = [f"{category[0]}. {category[1]}" for category in sql_output]
        return category_names

    def get_products(self):
        store = self.connect()

        cursor = store.cursor()
        cursor.execute("SELECT * FROM product")
        sql_output = cursor.fetchall()
        cursor.close()
        store.close()

        product_list = []
        for product in sql_output:
            product_dict = {}
            product_dict["id"] = product[0]
            product_dict["name"] = product[1]
            product_dict["description"] = product[2]
            product_dict["price"] = product[3]
            product_dict["quantity"] = product[4]
            product_dict["id_category"] = product[5]
            product_list.append(product_dict)

        return product_list

    def get_category_name(self, id_category):
        store = self.connect()
        cursor = store.cursor()
        cursor.execute("SELECT * FROM category")
        sql_output = cursor.fetchall()
        cursor.close()
        store.close()

        for category in sql_output:
            if category[0] == id_category:
                return category[1]
        return "Aucune"

    def create_new_product(self):
        store = self.connect()
        cursor = store.cursor()

        cursor.execute("SELECT id FROM product")
        sql_output = cursor.fetchall()
        id_list = []
        for product in sql_output:
            id_list.append(product[0])
        if len(id_list) == 0:
            increment_start = 1
        else:
            increment_start = max(id_list) + 1

        cursor.execute(f"ALTER TABLE product AUTO_INCREMENT = {increment_start}")
        store.commit()

        cursor.execute(
            "INSERT INTO product (name, description, price, quantity, id_category) "
            "VALUES ('Nouveau', 'Description', 0, 0, 0)"
        )
        store.commit()

        cursor.close()
        store.close()

    def delete_product(self, selected_id):
        if selected_id == None:
            return

        store = self.connect()
        cursor = store.cursor()

        cursor.execute(f"DELETE FROM product WHERE id = {selected_id}")
        store.commit()

        cursor.close()
        store.close()

    def get_attribute_value(self, attribute, product_id):
        store = self.connect()
        cursor = store.cursor()

        cursor.execute(f"SELECT {attribute} FROM product WHERE id = {product_id}")
        sql_output = cursor.fetchall()

        cursor.close()
        store.close()

        value = sql_output[0][0]
        return value

    def update_attribute_value(self, product_id, attribute, new_value):
        if isinstance(new_value, str):
            new_value = f"'{new_value}'"
        store = self.connect()
        cursor = store.cursor()

        cursor.execute(
            f"UPDATE product "
            f"SET {attribute} = {new_value} "
            f"WHERE id = {product_id}"
        )
        store.commit()

        cursor.close()
        store.close()


if __name__ == "__main__":
    store = Database("CV&$i7mx$oZDrq")
    result = store.get_products()
    print(result)