import unittest
from io import StringIO
import sys

class TestExamGrader(unittest.TestCase):

    def run_program_with_input(self, user_input):
        '''Runs the assignment.py program with the given input and returns the output.'''
        # Backup the original stdin and stdout
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        # Redirect stdin and stdout
        sys.stdin = StringIO(user_input)
        sys.stdout = StringIO()

        # Run the script
        try:
            from assignment import main  # Import the main function
            main()  # Call the main function
            output = sys.stdout.getvalue()  # Capture the output
        finally:
            # Restore the original stdin and stdout
            sys.stdin = original_stdin
            sys.stdout = original_stdout

        return output.strip()

    def test_all_correct_answers(self):
        output = self.run_program_with_input("adbdcacbdac\n")
        self.assertIn("Very Good!", output)
        self.assertIn("Your score is: 100 percent", output)

    def test_partial_correct_answers(self):
        output = self.run_program_with_input("adXdcaXXdXc\n")
        self.assertIn("You missed 4 questions: adXdcaXXdXc", output)
        self.assertIn("Your score is: 64 percent", output)

    def test_all_incorrect_answers(self):
        output = self.run_program_with_input("xxxxxxxxxxx\n")
        self.assertIn("You missed 11 questions: XXXXXXXXXXX", output)
        self.assertIn("Your score is: 0 percent", output)

    def test_invalid_input_length(self):
        user_inputs = iter(["abc\n", "adbdcacbdac\n"])  # First input is invalid, second is correct
        output = self.run_program_with_input("abc\nadbdcacbdac\n")
        self.assertIn("Error: an incorrect number of answers given.", output)
        self.assertIn("Very Good!", output)
        self.assertIn("Your score is: 100 percent", output)

if __name__ == "__main__":
    unittest.main()