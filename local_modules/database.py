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
        store = self.connect()
        if store.is_connected():
            return True
        else:
            return False
        store.close()


if __name__ == "__main__":
    store = Database("CV&$i7mx$oZDrq")
    result = store.check_connection()
    print(result)