import unittest

from shipping import shipping_cost


class ShippingTest(unittest.TestCase):
    def test_first_kilo(self):
        self.assertEqual(shipping_cost(0.5), 500)
        self.assertEqual(shipping_cost(1), 500)

    def test_each_extra_kilo(self):
        self.assertEqual(shipping_cost(2), 700)
        self.assertEqual(shipping_cost(3), 900)

    def test_partial_kilos_are_charged_as_full_kilo(self):
        self.assertEqual(shipping_cost(2.5), 900)
        self.assertEqual(shipping_cost(2.5), shipping_cost(3))
        self.assertEqual(shipping_cost(1.01), 700)


if __name__ == "__main__":
    unittest.main()
