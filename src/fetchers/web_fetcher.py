from urllib.parse import urlparse
from typing import Dict, Optional

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


"""Fetch job-description content from web pages."""

from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup

from src.models.fetched_job_page import FetchedJobPage


def _get_meta_content(
    soup: BeautifulSoup,
    *,
    name: Optional[str] = None,
    property_name: Optional[str] = None,
) -> Optional[str]:
    """Return content from a matching HTML meta tag."""

    attributes = {}

    if name is not None:
        attributes["name"] = name

    if property_name is not None:
        attributes["property"] = property_name

    tag = soup.find("meta", attrs=attributes)

    if tag is None:
        return None

    content = tag.get("content")

    if not isinstance(content, str):
        return None

    content = content.strip()

    return content or None


def _extract_metadata(
    soup: BeautifulSoup,
) -> Dict[str, str]:
    """Extract useful page-level metadata."""

    candidates = {
        "description": _get_meta_content(
            soup,
            name="description",
        ),
        "og:title": _get_meta_content(
            soup,
            property_name="og:title",
        ),
        "og:description": _get_meta_content(
            soup,
            property_name="og:description",
        ),
        "og:site_name": _get_meta_content(
            soup,
            property_name="og:site_name",
        ),
    }

    return {
        key: value
        for key, value in candidates.items()
        if value is not None
    }


def _extract_canonical_url(
    soup: BeautifulSoup,
) -> Optional[str]:
    """Extract the page's canonical URL."""

    tag = soup.find(
        "link",
        attrs={"rel": "canonical"},
    )

    if tag is None:
        return None

    href = tag.get("href")

    if not isinstance(href, str):
        return None

    href = href.strip()

    return href or None


def fetch_job_description(
    url: str,
) -> FetchedJobPage:
    """Fetch a job page and retain text plus page metadata."""

    validate_url(url)

    try:

        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(compatible; AI-Career-Manager/1.0)"
                )
            },
        )

        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(
            f"Failed to fetch job description: {e}"
        ) from e

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    for element in soup(
        ["script", "style", "noscript"]
    ):
        element.decompose()

    visible_text = soup.get_text(
        separator="\n",
        strip=True,
    )

    page_title = None

    if soup.title is not None:
        page_title = soup.title.get_text(
            strip=True
        ) or None

    return FetchedJobPage(
        requested_url=url,
        visible_text=visible_text,
        page_title=page_title,
        canonical_url=_extract_canonical_url(
            soup
        ),
        metadata=_extract_metadata(soup),
    )

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