from unittest.mock import Mock, patch

import pytest
import requests

from fetchers.web_fetcher import (
    extract_visible_text,
    fetch_job_description,
    validate_url,
)


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
    assert "Python and pytest" in result
    assert "Company navigation" not in result
    assert "console.log" not in result
    assert "Copyright information" not in result


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

    assert "SDET" in result
    assert "Build Python test automation" in result

    mock_get.assert_called_once()


@patch("fetchers.web_fetcher.requests.get")
def test_fetch_job_description_wraps_request_errors(mock_get):
    mock_get.side_effect = requests.RequestException(
        "Connection failed"
    )

    with pytest.raises(
        RuntimeError,
        match="Unable to download",
    ):
        fetch_job_description(
            "https://example.com/jobs/123"
        )