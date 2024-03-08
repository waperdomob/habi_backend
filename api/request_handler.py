from http.server import BaseHTTPRequestHandler
import json

class RequestHandler(BaseHTTPRequestHandler):
    """
    Clase para manejar las solicitudes HTTP y procesarlas para filtrar inmuebles.
    """
    def __init__(self, database, *args, **kwargs):
        """
        Constructor de la clase RequestHandler.

        Parámetros:
        - database: La instancia de la base de datos para realizar consultas.
        - *args: Argumentos posicionales adicionales para la clase base.
        - **kwargs: Argumentos de palabra clave adicionales para la clase base.
        """
        self.database = database
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """
        Maneja las solicitudes GET recibidas, procesa los datos de filtrado y devuelve los inmuebles filtrados.
        """
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            properties = self.get_filtered_properties(data)

            response = json.dumps(properties)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            self.wfile.write(response.encode())
        except Exception as e:
            self.send_error(500, message=str(e))

    def get_filtered_properties(self, data):
        """
        Filtra los inmuebles basados en los datos proporcionados.

        Parámetros:
        - data: Los datos de filtrado proporcionados por el cliente.

        Retorna:
        Una lista de inmuebles filtrados.
        """
        year_of_construction = data.get('year_of_construction')
        city = data.get('city')
        state = data.get('state')

        query, params = self.build_query(year_of_construction, city, state)
        results = self.execute_query(query, params)
        properties = self.format_results(results)

        return properties

    def build_query(self, year_of_construction, city, state):
        """
        Construye la consulta SQL basada en los datos de filtrado proporcionados.

        Parámetros:
        - year_of_construction: Año de construcción del inmueble.
        - city: Ciudad del inmueble.
        - state: Estado del inmueble.

        Retorna:
        La consulta SQL y los parámetros asociados.
        """

        query = """
            SELECT p.id, p.address, p.city, p.price, p.description, s.name
            FROM property p
            INNER JOIN status_history sh ON p.id = sh.property_id
            INNER JOIN status s ON sh.status_id = s.id
            WHERE s.name IN ('pre_venta', 'en_venta', 'vendido')
        """
        params = []

        if year_of_construction:
            query += "    AND p.year = %s"
            params.append(year_of_construction)
        if city:
            query += " AND p.city = %s"
            params.append(city)
        if state:
            query += " AND s.name = %s"
            params.append(state)

        return query, params

    def execute_query(self, query, params):
        """
        Ejecuta la consulta SQL en la base de datos.

        Parámetros:
        - query: La consulta SQL a ejecutar.
        - params: Los parámetros de la consulta.

        Retorna:
        Los resultados de la consulta.
        """
        try:
            return self.database.query(query, params)
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")

    def format_results(self, results):
        """
        Formatea los resultados de la consulta en el formato deseado.

        Parámetros:
        - results: Los resultados de la consulta.

        Retorna:
        Una lista de inmuebles formateados.
        """
        properties = [{'id': row[0], 'address': row[1], 'city': row[2], 'price': row[3], 'description': row[4], 'state': row[5]} for row in results]
        return properties


