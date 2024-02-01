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


if __name__ == "__main__":
    store = Database("CV&$i7mx$oZDrq")