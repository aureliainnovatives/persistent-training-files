import unittest
from inventory import find_product, total_inventory_value

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.products=[
            {"sku":"A","name":"Alpha","price":10.0,"quantity":2},
            {"sku":"B","name":"Beta","price":20.0,"quantity":3},
        ]

    def test_find_product(self):
        self.assertEqual(find_product(self.products,"B")["name"],"Beta")

    def test_missing_product(self):
        self.assertIsNone(find_product(self.products,"X"))

    def test_total_value(self):
        self.assertEqual(total_inventory_value(self.products),80.0)

if __name__=="__main__":
    unittest.main()
