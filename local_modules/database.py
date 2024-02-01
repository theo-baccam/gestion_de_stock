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
        cursor.execute("SELECT name FROM category")
        sql_output = cursor.fetchall()
        cursor.close()
        store.close()

        category_names = [category[0] for category in sql_output]
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


if __name__ == "__main__":
    store = Database("CV&$i7mx$oZDrq")
    store.get_products()