from django.test import TestCase
from django.core.exceptions import ValidationError
from password_validators.validators import NumberValidator, UppercaseValidator

class NumberValidatorTestCase(TestCase):
    def test_number_validator_invalid_string(self):
        validator = NumberValidator()
        with self.assertRaises(ValidationError) as context:
            validator.validate('abcdefg')

        self.assertTrue('The password must contain at least 1 digit, 0-9.' in str(context.exception))
    
    def test_number_validator_valid_string(self):
        validator = NumberValidator()
        valid = validator.validate('abcdefg123')
        self.assertEqual(valid, None)
        
    def test_number_validator_help_text(self):
        validator = NumberValidator()
        help_text = validator.get_help_text()
        self.assertEqual(help_text, "Your password must contain at least 1 digit.")
        
        
class UppsercaseValidatorTestCase(TestCase):
    def test_upper_case_validator_invalid_string(self):
        validator = UppercaseValidator()
        with self.assertRaises(ValidationError) as context:
            validator.validate('abcdefg')

        self.assertTrue('The password must contain at least 1 uppercase letter, A-Z.' in str(context.exception))
    
    def test_upper_case_validator_valid_string(self):
        validator = UppercaseValidator()
        valid = validator.validate('ABCDefg')
        self.assertEqual(valid, None)
        
    def test_upper_case_validator_help_text(self):
        validator = UppercaseValidator()
        help_text = validator.get_help_text()
        self.assertEqual(help_text, "Your password must contain at least 1 uppercase letter.")
