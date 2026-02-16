import pytest

from text_toolkit.extractors.base import Extractor
from text_toolkit.extractors.core import EmailExtractor


@pytest.mark.parametrize(
    "text, expected_emails",
    [
        ("Contact mail: admin@example.com", ["admin@example.com"]),
        (
            "Contactos: admin@example.com, support@test.com, info@company.org",
            ["admin@example.com", "support@test.com", "info@company.org"],
        ),
        ("Email: user+tag@example.com", ["user+tag@example.com"]),
        (
            """
            Project contact team:
            - Administrator: admin@example.com
            - Technical Support: support@example.com.mx
            - Sales: sales.team@company.co.uk
            - Development: dev+backend@tech-startup.io
            - Marketing: contact_marketing@agency.com
            For more information: info@help-center.org
            """,
            [
                "admin@example.com",
                "support@example.com.mx",
                "sales.team@company.co.uk",
                "dev+backend@tech-startup.io",
                "contact_marketing@agency.com",
                "info@help-center.org",
            ],
        ),
    ],
    ids=[
        "single_email",
        "multiple_emails",
        "plus_sign_tag",
        "multiple_email_patterns",
    ],
)
def test_email_extractor(email_extractor: Extractor, text: str, expected_emails: list[str]):
    extracted_data = email_extractor.extract(text)

    assert isinstance(extracted_data, list), "Data structure should be a List"
    assert len(extracted_data) == len(expected_emails), (
        "Size of extracted data doesnt match expected_emails size"
    )
    assert extracted_data == expected_emails, f"Emails extracted should be {expected_emails}"


def test_email_extractor_repr_includes_pattern_information() -> None:
    extractor = EmailExtractor()

    representation = repr(extractor)

    assert "EmailExtractor" in representation
    assert "patterns_amount=" in representation
