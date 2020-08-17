import unittest

from subnet import calculate_subnet, EmptyIPList


class TestSubnetCalculator(unittest.TestCase):
    """Ключевые тесты функции вычисления подсети."""

    def test_25_bit_mask(self):
        """Тест для адресов подсети с 25 битной маской."""

        self.assertEqual(
            calculate_subnet(
                ['192.168.1.126', '192.168.1.4', '192.168.1.12', '192.168.1.50']
            ),
            '192.168.1.0/25'
        )

    def test_16_bit_mask(self):
        """Тест для адресов подсети с 16 битной маской."""

        self.assertEqual(
            calculate_subnet(
                ['192.168.128.128', '192.168.15.66', '192.168.222.123']
            ),
            '192.168.0.0/16'
        )

    def test_0_bit_mask(self):
        """Тест для адресов подсети с 0 битной маской."""

        self.assertEqual(
            calculate_subnet(
                ['1.168.128.128', '15.168.15.66', '192.168.222.123']
            ),
            '0.0.0.0/0'
        )

    def test_subnet_for_one_address(self):
        """Тест для списка из одного адреса."""

        self.assertEqual(calculate_subnet(['192.168.1.192']), '192.168.1.192/32')

    def test_empty_list(self):
        """Тест проверки передаваемого списка на пустоту."""

        with self.assertRaises(EmptyIPList) as context_manager:
            calculate_subnet([])
        self.assertEqual(context_manager.exception.message, 'IP list is empty')

    def test_invalid_argument_type(self):
        """Тест валидации типа передаваемого аргумента."""

        with self.assertRaises(TypeError) as context_manager:
            calculate_subnet({'192.168.1.192'})
        self.assertEqual(context_manager.exception.args[0], 'ip_addresses is not list')


if __name__ == "__main__":
    unittest.main()
