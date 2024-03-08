from http.server import HTTPServer
from request_handler import RequestHandler
from database.connection_db import Database

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    """
    Función para iniciar el servidor HTTP y manejar las solicitudes entrantes.

    Parámetros:
    - server_class: La clase del servidor a utilizar.
    - handler_class: La clase del manejador de solicitudes a utilizar.
    - port: El puerto en el que se ejecutará el servidor (predeterminado: 8000).
    """

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        print(f'Starting server on port {port}...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the server')
        httpd.server_close()

if __name__ == '__main__':
    db_config = {
        'user': 'pruebas',
        'password': 'VGbt3Day5R',
        'host': '3.138.156.32',
        'database': 'habi_db',
        'port': 3309
    }
    database = Database(db_config)
    run(handler_class=lambda *args, **kwargs: RequestHandler(database, *args, **kwargs))
