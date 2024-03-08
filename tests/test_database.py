import unittest
from api.database.connection_db import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db_config = {
            'user': 'pruebas',
            'password': 'VGbt3Day5R',
            'host': '3.138.156.32',
            'database': 'habi_db',
            'port': 3309
        }
        self.database = Database(self.db_config)

    def tearDown(self):
        self.database.close()

    def test_query(self):
        query = ("SELECT * FROM status_history")
        results = self.database.query(query)
        self.assertGreater(len(results), 0)

if __name__ == '__main__':
    unittest.main()