from io import BytesIO
import unittest
from http.server import BaseHTTPRequestHandler
from unittest.mock import MagicMock
from api.request_handler import RequestHandler


class MockRequest(BaseHTTPRequestHandler):
    def __init__(self, data):
        self.rfile = BytesIO(data)
        self.rfile.headers = {'Content-Length': len(data)}
        self.connection = MagicMock()

    def makefile(self, *args, **kwargs):
        return BytesIO()

class TestRequestHandler(unittest.TestCase):
    def setUp(self):
        self.database = MagicMock()
        self.request_data = b'{"year_of_construction": 2020, "city": "Bogota", "state": "pre_venta"}'
        self.client_address_mock = ('127.0.0.1', 12345)
        self.server_mock = MagicMock()

        
    def test_build_query(self):
        request = MockRequest(self.request_data)
        handler = RequestHandler(database=self.database, request=request, client_address=self.client_address_mock, server=self.server_mock)
        # Definir datos de prueba
        year_of_construction = "2020"
        city = "Bogotá"
        state = "pre_venta"

        query, params = handler.build_query(year_of_construction, city, state)

        expected_query = """
            SELECT p.id, p.address, p.city, p.price, p.description, s.name
            FROM property p
            INNER JOIN status_history sh ON p.id = sh.property_id
            INNER JOIN status s ON sh.status_id = s.id
            WHERE s.name IN ('pre_venta', 'en_venta', 'vendido')
            AND p.year = %s AND p.city = %s AND s.name = %s
        """
        expected_params = ["2020", "Bogotá", "pre_venta"]

        self.assertEqual(query.strip(), expected_query.strip())
        self.assertEqual(params, expected_params)

    def test_execute_query(self):
        request = MockRequest(self.request_data)
        handler = RequestHandler(database=self.database, request=request, client_address=self.client_address_mock, server=self.server_mock)
        
        query = "SELECT * FROM property"
        params = [1, 2, 3]

        handler.database.query.return_value = [("result",)]

        results = handler.execute_query(query, params)

        handler.database.query.assert_called_once_with(query, params)

        self.assertEqual(results, [("result",)])

if __name__ == '__main__':
    unittest.main()