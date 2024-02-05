# Tout ce qui concerne la database et le traitement des données des tables
import mysql.connector


class Database:
    def __init__(self, password):
        if not isinstance(password, str):
            raise ValueError("Le mot de passe doit être un string")

        self.password = password

    # Méthode pour se connecter
    def connect(self):
        # skip reformat avec black
        # fmt: off
        store = mysql.connector.connect(
            host="localhost",
            user="root",
            password=self.password,
            database="store"
        )
        return store
        # fmt: on

    # Pour vérifier si connecté, utilisé dans écran mot de passe
    def check_connection(self):
        try:
            store = self.connect()
            store.close()
            return True
        except:
            return False

    # Pour créer un nouveau produit
    def create_new_product(self):
        store = self.connect()
        cursor = store.cursor()

        # Pour reset l'auto_increment et empêcher des skips
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

    # Pour obtenir ID et nom de catégorie, utilisé pour choix de catégorie
    def get_categories(self):
        store = self.connect()

        cursor = store.cursor()
        cursor.execute("SELECT * FROM category")
        sql_output = cursor.fetchall()
        cursor.close()
        store.close()

        category_names = [f"{category[0]}. {category[1]}" for category in sql_output]
        return category_names

    # Pour obtenir les noms de catégorie selon l'id_category du produit.
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

    # Pour obtenir les produits
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

    # Pour obtenir la valeur d'un attribut d'un produit
    def get_attribute_value(self, attribute, product_id):
        store = self.connect()
        cursor = store.cursor()

        cursor.execute(f"SELECT {attribute} FROM product WHERE id = {product_id}")
        sql_output = cursor.fetchall()

        cursor.close()
        store.close()

        value = sql_output[0][0]
        return value

    # Pour mettre à jour un attribut d'un produit
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

    # Pour supprimer un produit
    def delete_product(self, selected_id):
        if selected_id == None:
            return

        store = self.connect()
        cursor = store.cursor()

        cursor.execute(f"DELETE FROM product WHERE id = {selected_id}")
        store.commit()

        cursor.close()
        store.close()
