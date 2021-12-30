from unittest import TestCase
from unittest.mock import patch

from time_attack.utils import yes_or_no


class TestUtils(TestCase):
    def test_yes_or_no(self):

        msg = "abcd"

        expected_msg = "abcd (y/n) "
        with patch("builtins.input") as mock_input:

            mock_input.return_value = "y"

            answer = yes_or_no(msg)

            mock_input.assert_called_with(expected_msg)

            self.assertTrue(answer)

            mock_input.return_value = "Y"

            answer = yes_or_no(msg)

            self.assertTrue(answer)

            mock_input.return_value = "n"

            answer = yes_or_no(msg)

            self.assertFalse(answer)

            mock_input.return_value = "N"

            answer = yes_or_no(msg)

            self.assertFalse(answer)

            mock_input.reset_mock()

            mock_input.side_effect = ("Nein", "y")

            answer = yes_or_no(msg)

            self.assertEqual(mock_input.call_count, 2)

            self.assertTrue(answer)
