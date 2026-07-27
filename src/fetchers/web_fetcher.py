from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


DEFAULT_TIMEOUT_SECONDS = 15

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/126.0 Safari/537.36"
    )
}


def fetch_job_description(url: str) -> str:
    """
    Download a web page and return its visible text.

    This initial implementation works best with static HTML pages.
    JavaScript-rendered job sites may require a browser-based fetcher later.

    Args:
        url: Public HTTP or HTTPS URL containing a job posting.

    Returns:
        Extracted visible page text.

    Raises:
        ValueError: If the URL is invalid or no useful text is found.
        RuntimeError: If the page cannot be downloaded.
    """
    validate_url(url)

    try:
        response = requests.get(
            url,
            headers=REQUEST_HEADERS,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Unable to download job posting from {url}: {exc}"
        ) from exc

    text = extract_visible_text(response.text)

    if not text:
        raise ValueError(
            f"No readable job-description text was found at {url}"
        )

    return text


def validate_url(url: str) -> None:
    """
    Validate that a URL uses HTTP or HTTPS and includes a hostname.
    """
    parsed_url = urlparse(url)

    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError(
            "Job URL must begin with http:// or https://"
        )

    if not parsed_url.netloc:
        raise ValueError(
            f"Job URL does not contain a valid hostname: {url}"
        )


def extract_visible_text(html: str) -> str:
    """
    Extract readable text from an HTML document.
    """
    soup = BeautifulSoup(html, "html.parser")

    for element in soup(
        [
            "script",
            "style",
            "noscript",
            "svg",
            "nav",
            "footer",
        ]
    ):
        element.decompose()

    page_text = soup.get_text(
        separator="\n",
        strip=True,
    )

    lines = [
        line.strip()
        for line in page_text.splitlines()
        if line.strip()
    ]

    return "\n".join(lines)