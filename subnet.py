import socket
import struct
from typing import List
import unittest


class EmptyIPList(Exception):
    """Исключение для обработки пустого списка."""

    message = 'IP list is empty'


def calculate_subnet(ip_addresses: List[str]):
    """Метод вычисления минимальной подсети для набора IP адресов.

    :param ip_addresses: список IP адресов в строковом виде, с октетами, разделенными точками.
    :return: адрес подсети для набора полученных адресов.
    """

    def str_ip_to_integer(ip_string: str):
        """Шорткат для преобразования строки IP адреса в целое значение.

        :param ip_string: IP адрес в строковом виде, с октетами, разделенными точками.
        :return: адрес в виде целого числа.
        """

        return struct.unpack('!I', socket.inet_aton(ip_string))[0]

    def integer_ip_to_str(ip_integer: int):
        """Шорткат для преобразования целого значения IP адреса в строковое представление.

        :param ip_integer: IP адрес в виде числа.
        :return: IP адрес в строковом виде, с октетами, разделенными точками.
        """

        return socket.inet_ntoa(struct.pack('!L', ip_integer))

    if not ip_addresses:
        raise EmptyIPList

    if not isinstance(ip_addresses, list):
        raise TypeError('ip_addresses is not list')

    differences = {0}
    first_ip_integer_format = str_ip_to_integer(ip_addresses[0])
    for ip in ip_addresses[1:]:
        ip_integer_format = str_ip_to_integer(ip)
        differences.add((first_ip_integer_format ^ ip_integer_format).bit_length())
    maximum_difference_length = max(differences)
    mask_size = 32 - maximum_difference_length
    subnet_address = first_ip_integer_format & ((2 ** mask_size - 1) << maximum_difference_length)
    return f'{integer_ip_to_str(subnet_address)}/{mask_size}'


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
