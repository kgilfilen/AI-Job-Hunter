from unittest.mock import Mock, patch

import pytest
import requests

from bs4 import BeautifulSoup

from src.fetchers.web_fetcher import (
    fetch_job_description,
    _extract_canonical_url,
    _extract_metadata,
    validate_url,
    extract_visible_text,
)

HTML = """
<html>
<head>
    <title>Senior SDET | Applied Systems</title>

    <link
        rel="canonical"
        href="https://www.appliedsystems.com/jobs/sdet"
    >

    <meta
        name="description"
        content="Join Applied Systems as a Senior SDET."
    >

    <meta
        property="og:title"
        content="Senior SDET"
    >

    <meta
        property="og:site_name"
        content="Applied Systems"
    >
</head>
<body>
    <h1>Senior Software Development Engineer in Test</h1>
</body>
</html>
"""

def test_validate_url_accepts_https():
    validate_url("https://example.com/jobs/123")


def test_validate_url_rejects_missing_scheme():
    with pytest.raises(
        ValueError,
        match="must begin with",
    ):
        validate_url("example.com/jobs/123")


def test_validate_url_rejects_unsupported_scheme():
    with pytest.raises(
        ValueError,
        match="must begin with",
    ):
        validate_url("ftp://example.com/jobs/123")


def test_extract_visible_text_removes_script_and_navigation():
    html = """
    <html>
        <body>
            <nav>Company navigation</nav>
            <script>console.log("ignore this")</script>
            <main>
                <h1>Senior QA Automation Engineer</h1>
                <p>Experience with Python and pytest required.</p>
            </main>
            <footer>Copyright information</footer>
        </body>
    </html>
    """

    result = extract_visible_text(html)

    assert "Senior QA Automation Engineer" in result
    assert "Experience with Python and pytest required." in result
    assert "Company navigation" not in result
    assert "console.log" not in result
    assert "Copyright information" not in result
    assert "Python and pytest" in result


@patch("fetchers.web_fetcher.requests.get")
def test_fetch_job_description_returns_page_text(mock_get):
    response = Mock()
    response.text = """
    <html>
        <body>
            <main>
                <h1>SDET</h1>
                <p>Build Python test automation.</p>
            </main>
        </body>
    </html>
    """
    response.raise_for_status.return_value = None
    mock_get.return_value = response

    result = fetch_job_description(
        "https://example.com/jobs/123"
    )

    assert "SDET" in result.visible_text
    assert "Build Python test automation" in result.visible_text

    mock_get.assert_called_once()


@patch("src.fetchers.web_fetcher.requests.get")
def test_fetch_job_description_wraps_request_errors(
    mock_get,
) -> None:
    mock_get.side_effect = requests.RequestException(
        "Connection failed"
    )

    with pytest.raises(
        RuntimeError,
        match="Failed to fetch job description",
    ):
        fetch_job_description(
            "https://example.com/job"
        )
        
def test_extract_page_metadata() -> None:
    soup = BeautifulSoup(
        HTML,
        "html.parser",
    )

    metadata = _extract_metadata(soup)

    assert metadata["description"] == (
        "Join Applied Systems as a Senior SDET."
    )
    assert metadata["og:title"] == "Senior SDET"
    assert metadata["og:site_name"] == (
        "Applied Systems"
    )


def test_extract_canonical_url() -> None:
    soup = BeautifulSoup(
        HTML,
        "html.parser",
    )

    assert _extract_canonical_url(soup) == (
        "https://www.appliedsystems.com/jobs/sdet"
    )

@patch("src.fetchers.web_fetcher.requests.get")
def test_fetch_job_description_returns_page_evidence(
    mock_get,
) -> None:
    response = Mock()
    response.text = HTML
    response.raise_for_status.return_value = None

    mock_get.return_value = response

    result = fetch_job_description(
        "https://example.com/posting"
    )

    assert result.requested_url == (
        "https://example.com/posting"
    )
    assert result.page_title == (
        "Senior SDET | Applied Systems"
    )
    assert result.canonical_url == (
        "https://www.appliedsystems.com/jobs/sdet"
    )
    assert "Senior Software Development Engineer" in (
        result.visible_text
    )
    assert result.metadata["og:site_name"] == (
        "Applied Systems"
    )
