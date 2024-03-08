import mysql.connector

class Database:
    """
    Clase para manejar la conexión a la base de datos y ejecutar consultas.
    """
    _instance = None

    def __new__(cls, config):
        """
        Crea una instancia única de la clase Database si aún no existe.

        Parámetros:
        - cls: La clase Database.
        - config: Un diccionario que contiene la configuración de conexión.

        Retorna:
        La instancia única de la clase Database.
        """
         
        if cls._instance is None:
            try:
                cls._instance = super().__new__(cls)
                cls._instance.cnx = mysql.connector.connect(**config)
                cls._instance.cursor = cls._instance.cnx.cursor()
            except mysql.connector.Error as err:
                raise ConnectionError(f"Error connecting to database: {err}")
            except AttributeError as attr_err:
                raise AttributeError(f"Attribute error: {attr_err}")
        return cls._instance

    def query(self, query, params=None):
        """
        Ejecuta una consulta SQL en la base de datos.

        Parámetros:
        - self: La instancia de la clase Database.
        - query: La consulta SQL a ejecutar.
        - params: Los parámetros de la consulta (predeterminado: None).

        Retorna:
        Los resultados de la consulta.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            raise RuntimeError(f"Error executing query: {err}")

    def close(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.cursor.close()
        self.cnx.close()
