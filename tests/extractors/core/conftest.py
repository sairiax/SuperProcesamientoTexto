"""Shared fixtures for core extractor tests."""

import pytest

from text_toolkit.extractors.core import (
    CustomExtractor,
    DateExtractor,
    EmailExtractor,
    URLExtractor,
)


@pytest.fixture
def email_extractor():
    """Fixture that provides an EmailExtractor instance."""
    return EmailExtractor()


@pytest.fixture
def url_extractor():
    """Fixture that provides a URLExtractor instance."""
    return URLExtractor()


@pytest.fixture
def date_extractor():
    """Fixture that provides a DateExtractor instance."""
    return DateExtractor()


@pytest.fixture
def custom_phone_extractor():
    """Fixture that provides a CustomExtractor pre-configured for phone patterns."""
    return CustomExtractor(
        name="phone",
        patterns=[r"\d{3}-\d{3}-\d{4}", r"\(\d{3}\)\s*\d{3}-\d{4}"],
    )


@pytest.fixture
def custom_ip_extractor():
    """Fixture that provides a CustomExtractor pre-configured for IP addresses."""
    return CustomExtractor(
        name="ip_address",
        patterns=[r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"],
    )
