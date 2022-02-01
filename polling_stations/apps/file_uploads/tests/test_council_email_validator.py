from django.core.exceptions import ValidationError
from django.test import TestCase

from file_uploads.forms import CouncilEmailValidator


class CouncilEmailValidatorTest(TestCase):
    def setUp(self):
        self.council_email_validator = CouncilEmailValidator()

    def test_dem_club(self):
        self.assertIsNone(self.council_email_validator("foo@democracyclub.org.uk"))

    def test_ec(self):
        self.assertIsNone(
            self.council_email_validator("foo@electoralcommission.org.uk")
        )

    def test_fake_dem_club(self):
        with self.assertRaises(ValidationError):
            self.council_email_validator("foo@fakedemocracyclub.org.uk")

    def test_gov_uk(self):
        self.council_email_validator = CouncilEmailValidator()
        self.assertIsNone(self.council_email_validator("foo@bar.gov.uk"))

    def test_fake_gov_uk(self):
        with self.assertRaises(ValidationError):
            self.council_email_validator("foo@bar.gov.uk.fake")
