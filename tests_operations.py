import unittest
import server


class TestOperations(unittest.TestCase):

    def test_operation_null_array(self):
        with self.assertRaises(Exception) as context:
            server.evaluate_rpn(None)
        self.assertEqual(str(context.exception), "L'expression a evaluer est nulle ou vide.")

    def test_operation_empty_array(self):
        with self.assertRaises(Exception) as context:
            server.evaluate_rpn("")
        self.assertEqual(str(context.exception), "L'expression a evaluer est nulle ou vide.")

    # (1 + 2) * (3 + 4) = 1 2 + 3 4 + *
    def test_operation_valid_simple_array1(self):
        expression = ['1', '2', '+', '3', '4', '+', '*']
        result = server.evaluate_rpn(expression)
        self.assertTrue(result == 21)

    # 2 * 4 + 8 = 16
    def test_operation_valid_simple_array2(self):
        expression = ['2', '4', '*', '8', '+']
        result = server.evaluate_rpn(expression)
        self.assertTrue(result == 16)

    # (1 + 2) / 3 = 1 2 + 3 /
    def test_operation_valid_simple_array3(self):
        expression = ['1', '2', '+', '3', '/']
        result = server.evaluate_rpn(expression)
        self.assertTrue(result == 1)

    # (10 + (4 * 2)) / 9 = 10 4 2 * + 9 /
    def test_operation_complex_array1(self):
        expression = ['10', '4', '2', '*', '+', '9', '/']
        result = server.evaluate_rpn(expression)
        self.assertTrue(result == 2)

    # (15 / (7 - (1 + 1))) * 3 - (2 + (1 + 1)) = 15 7 1 1 + - / 3 * 2 1 1 + + -
    def test_operation_complex_array2(self):
        expression = ['15', '7', '1', '1', '+', '-', '/', '3', '*', '2', '1', '1', '+', '+', '-']
        result = server.evaluate_rpn(expression)
        self.assertTrue(result == 5)

    # ((5 + 1) * (2 + 1)) ^ 2 = 5 1 + 2 1 + * 2 ^
    def test_operation_complex_array3(self):
        expression = ['5', '1', '+', '2', '1', '+', '*', '2', '^']
        result = server.evaluate_rpn(expression)
        self.assertTrue(result == 324)

    # 3 + 4 * 2 / (1 - 5) ^ 2 ^ 3 = 3 4 2 * 1 5 - 2 3 ^ ^ / +
    def test_operation_complex_array4(self):
        expression = ['3', '4', '2', '*', '1', '5', '-', '2', '3', '^', '^', '/', '+']
        result = server.evaluate_rpn(expression)
        self.assertTrue(result == 3.0001220703125)

    def test_operation_invalid_array(self):
        expression = ['4', '2', '*', '1', '3', '+', '*', '+']
        with self.assertRaises(ValueError) as context:
            server.evaluate_rpn(expression)
        self.assertEqual(str(context.exception), "Invalid RPN expression: not enough operands in the stack.")

    # (1+1) / (1-1) = 1 1 + 1 1 - /
    def test_operation_division_par_zero(self):
        expression = ['1', '1', '+', '1', '1', '-', '/']
        with self.assertRaises(ValueError) as context:
            server.evaluate_rpn(expression)
        self.assertEqual(str(context.exception), "Division par zero.")

    # a + 1 = a 1 +
    def test_operation_on_invalid_token(self):
        expression = ['a', '1', '+']
        with self.assertRaises(ValueError) as context:
            server.evaluate_rpn(expression)
        self.assertEqual(str(context.exception), "Invalid token.")
